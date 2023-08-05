from setuptools import setup, find_packages

setup(
    name="chinachess",
    version="1.0",
    author="lindengxu68",
    author_email="lindengxu68@gmail.com",
    description="chinachess",

    # 项目主页
    url="https://github.com/lindengxu68/chess", 

    # 你要安装的包，通过 setuptools.find_packages 找到当前目录下有哪些包
    packages=find_packages(),
    package_data={
        's1':['imgs/s1/*.png'],
        's2':['imgs/s2/*.png']
               },
    python_requires='>=3',
    install_requires=['pygame']
)