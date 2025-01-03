from setuptools import find_packages
from setuptools import setup

setup(
    name="zfuns",
    setup_requires=["setuptools_scm"],
    use_scm_version=True,  # git tag 1.0.0, 自动获取版本号
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
