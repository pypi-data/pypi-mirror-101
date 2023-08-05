from setuptools import setup, find_namespace_packages

setup(
    name="chinachess",
    version="1.1",
    author="lindengxu68",
    author_email="lindengxu68@gmail.com",
    description="chinachess",
    # 项目主页
    url="https://github.com/lindengxu68/chess", 
packages=find_namespace_packages(
                     include=["code", "imgs"], ),
    python_requires='>=3',
    install_requires=['pygame'],
    include_package_data=True
)