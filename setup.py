from setuptools import setup, find_packages

requires = [
    'certifi>=2019.6.16',
    'chardet>=3.0.4',
    'idna>=2.8',
    'Pygments>=2.4.2',
    'requests>=2.22.0',
    'urllib3>=1.25.3'
]

setup(
    name='FtApi',
    version='1.9.8', 
    author="ryaoi",
    author_email="nop@42.codes",
    url="https://github.com/ryaoi/ftApi",
    license='LICENSE.txt',
    description='Class for manipulating 42 Api',
    long_description=open('README.md').read(),
    install_requires=requires,
    packages=find_packages())
