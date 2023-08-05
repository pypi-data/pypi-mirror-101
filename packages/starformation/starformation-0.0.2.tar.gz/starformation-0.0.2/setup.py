import setuptools

setuptools.setup(
    name="starformation",
    version="0.0.2",
    author="Tommy Dong",
    author_email="tommydong1998@gmail.com",
    description="Star Formation is a Python library to quickly develop clean modular models/pipelines.",
    long_description="Star Formation is a Python library to quickly develop clean modular models/pipelines. Geared towards usage with sklearn and keras.",
    long_description_content_type="text/markdown",
    url="https://github.com/TommyDong1998/StarFormation",
    packages=['starformation','starformation.classic'],
    install_requires=['backtrader','requests','matplotlib']
)