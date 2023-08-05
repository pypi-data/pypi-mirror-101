import setuptools
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="starformation",
    version="0.0.3",
    author="Tommy Dong",
    author_email="tommydong1998@gmail.com",
    description="Star Formation is a Python library to quickly develop clean modular models/pipelines.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TommyDong1998/StarFormation",
    packages=['starformation','starformation.classic'],
    install_requires=['backtrader','pathos']
)