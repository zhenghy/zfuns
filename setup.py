from setuptools import find_packages
from setuptools import setup

setup(
    name="zfuns",
    version="2.0.3",
    author="Haiyang Zheng",
    author_email="wnfdsfy@gmail.com",
    packages=find_packages(),
    url="https://github.com/zhenghy/zfuns",
    license="MIT",
    description="个人常用函数库",
    long_description=open("README.MD", "r").read(),
    long_description_content_type="text/markdown",
    install_requires=[
        "pymysql",
        "pywinrm",
        "sqlalchemy",
    ],
    keywords=["common", "function", "class"],
    platforms="any",
)
