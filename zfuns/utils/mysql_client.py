import re
from dataclasses import dataclass
from dataclasses import field
from typing import List
from typing import Tuple

import polars as pl
import pymysql
import sqlalchemy


@dataclass
class MySQLClient:
    """MySQL 数据库客户端，用于处理数据库操作"""

    host: str
    user: str
    password: str
    database: str
    engine: sqlalchemy.Engine = field(init=False)

    def __post_init__(self):
        """初始化后创建 SQLAlchemy 引擎"""
        self.engine = self._create_engine()

    def _create_engine(self) -> sqlalchemy.Engine:
        """创建用于数据库连接的 SQLAlchemy 引擎"""
        connection_string = (
            f"mysql+pymysql://{self.user}:{self.password}"
            f"@{self.host}:3306/{self.database}"
        )
        return sqlalchemy.create_engine(connection_string)

    def _get_connection(self) -> pymysql.cursors.Cursor:
        """创建并返回数据库连接游标

        返回:
            数据库游标对象

        异常:
            SystemExit: 如果连接失败
        """
        if not self.database:
            raise SystemExit("未指定数据库。")

        try:
            connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                use_unicode=True,
                charset="utf8",
            )
        except Exception as e:
            print(f"数据库连接错误: {e}")
            raise SystemExit("无法连接到 MySQL 数据库。")

        cursor = connection.cursor()
        if not cursor:
            raise SystemExit("无法创建数据库游标")

        return cursor

    @staticmethod
    def _clean_sql(sql: str) -> str:
        """移除 SQL 查询中的多余空格和换行

        参数:
            sql: SQL 查询字符串

        返回:
            清理后的 SQL 查询
        """
        return re.sub(r"\s*\n\s*", " ", sql)

    def execute_query(self, sql: str) -> Tuple[Tuple[str, ...], ...]:
        """执行 SELECT 查询并返回结果和列名

        参数:
            sql: SELECT 查询字符串

        返回:
            包含列名和查询结果的元组
        """
        cursor = self._get_connection()
        cursor.execute(sql)
        results = cursor.fetchall()
        column_names = tuple(column[0] for column in cursor.description)
        cursor.connection.close()

        return (column_names,) + results

    def execute_non_query(self, sql_list: List[str]) -> bool:
        """执行一组非查询 SQL 语句 (INSERT, UPDATE, DELETE)

        参数:
            sql_list: 要执行的 SQL 语句列表

        返回:
            成功返回 True，失败返回 False
        """
        cursor = self._get_connection()
        connection = cursor.connection

        try:
            for sql in sql_list:
                cursor.execute(sql)
            connection.commit()
            success = True
        except Exception as e:
            print(f"执行 SQL 时出错: {e}")
            connection.rollback()
            success = False
        finally:
            connection.close()

        return success

    @staticmethod
    def generate_upsert_sql(
        table: str, columns: List[str], values: List[str]
    ) -> str:
        """生成用于 INSERT ... ON DUPLICATE KEY UPDATE 的 SQL

        参数:
            table: 目标表名
            columns: 列名列表
            values: 值元组的字符串列表

        返回:
            用于 upsert 操作的 SQL 查询字符串
        """
        if not columns or not values:
            return ""

        quoted_columns = [f"`{col}`" for col in columns]
        value_string = ",\n".join(values)
        update_clauses = [f"{col}=VALUES({col})" for col in quoted_columns]

        sql = f"""
            INSERT INTO {table} ({','.join(quoted_columns)})
            VALUES {value_string}
            ON DUPLICATE KEY UPDATE {','.join(update_clauses)}
        """
        return re.sub(r"\s*\n\s*", "\n", sql)

    def dataframe_to_database(self, df: pl.DataFrame, table: str) -> str:
        """将 DataFrame 内容插入或更新到数据库表中

        参数:
            df: 源 DataFrame
            table: 目标表名

        返回:
            执行的 SQL 查询
        """
        # 清理并准备 DataFrame
        df = df.fill_null("")
        df = df.select(
            [col for col in df.columns if not df[col].is_null().all()]
        )
        df = df.with_columns(df.select(pl.all().cast(pl.Utf8)))

        # 匹配 DataFrame 列与数据库列
        db_columns = set(
            self.execute_query(f"SELECT * FROM {table} LIMIT 1")[0]
        )
        df = df.select([col for col in df.columns if col in db_columns])

        # 生成 SQL 值
        sql_values = []
        for row in df.iter_rows(named=True):
            value_string = "('" + "','".join(row.values()) + "')"
            sql_values.append(value_string)

        # 执行 upsert
        sql = self.generate_upsert_sql(table, df.columns, sql_values)
        if sql:
            self.execute_non_query([sql])
        return sql

    def update_table_from_dataframe(
        self,
        df: pl.DataFrame,
        table: str,
        match_columns: List[str],
        key_columns: List[str],
        condition: str = "1=1",
    ) -> pl.DataFrame:
        """使用 DataFrame 数据更新数据库表

        参数:
            df: 源 DataFrame
            table: 目标表名
            match_columns: 用于匹配更新的列
            key_columns: 主键/唯一键列
            condition: 额外的 WHERE 子句条件

        返回:
            更新后的 DataFrame
        """
        # 从数据库获取现有数据
        quoted_keys = ",".join(f"`{col}`" for col in key_columns)
        sql = f"SELECT {quoted_keys} FROM {table} WHERE {condition}"
        db_data = pl.from_pandas(
            pl.read_sql(sql, self.engine)
        )  # polars read sql??

        # 删除 db_data 中存在于 df 但不在 match_columns 中的列
        columns_to_drop = [
            col
            for col in db_data.columns
            if col not in match_columns and col in df.columns
        ]
        db_data = db_data.drop(columns_to_drop)

        # 合并并更新
        merged_data = df.join(db_data, on=match_columns, how="left")
        self.dataframe_to_database(merged_data, table)

        return merged_data


def test_mysql_client():
    # 初始化 MySQLClient
    print("初始化 MySQLClient...")
    client = MySQLClient(
        host="127.0.0.1",
        user="root",
        password="123",
        database="test",
    )
    print("MySQLClient 初始化完成。")

    # 测试 execute_query 方法
    print("\n测试 execute_query 方法...")
    query = "SELECT * FROM test_table LIMIT 1"
    print(f"执行查询: {query}")
    try:
        result = client.execute_query(query)
        print("查询成功。")
        print("结果:", result)
    except Exception as e:
        print("执行查询时出错:", e)

    # 测试 execute_non_query 方法
    print("\n测试 execute_non_query 方法...")
    non_query = [
        "INSERT INTO test_table (id, name, value) VALUES (1, 'test', '100')"
    ]
    print(f"执行非查询: {non_query}")
    try:
        success = client.execute_non_query(non_query)
        print("非查询执行成功。" if success else "非查询执行失败。")
    except Exception as e:
        print("执行非查询时出错:", e)

    # 测试 dataframe_to_database 方法
    print("\n测试 dataframe_to_database 方法...")
    data = {"id": [2], "name": ["test2"], "value": ["200"]}
    df = pl.DataFrame(data)
    print("要插入的 DataFrame:", df)
    try:
        sql = client.dataframe_to_database(df, "test_table")
        print("DataFrame 插入成功。")
        print("执行的 SQL:", sql)
    except Exception as e:
        print("插入 DataFrame 时出错:", e)

    # 测试 update_table_from_dataframe 方法
    print("\n测试 update_table_from_dataframe 方法...")
    update_data = {"id": [1], "name": ["test"], "value": ["150"]}
    update_df = pl.DataFrame(update_data)
    print("要更新的 DataFrame:", update_df)
    try:
        updated_df = client.update_table_from_dataframe(
            update_df, "test_table", ["id"], ["id"]
        )
        print("DataFrame 更新成功。")
        print("更新后的 DataFrame:", updated_df)
    except Exception as e:
        print("更新 DataFrame 时出错:", e)


if __name__ == "__main__":
    test_mysql_client()
