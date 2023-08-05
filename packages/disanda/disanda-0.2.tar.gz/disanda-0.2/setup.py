#from distutils.core import setup
from setuptools import find_packages,setup

name='disanda'
setup(
    name=name, 
    version='0.2',
    py_modules =[name], #这个要跟发布的模块名一致
    author='disanda',
    author_email='disanda@foxmail.com',
    url='http://disanda.github.io',
    description='2th issue',
    packages = find_packages()
)

