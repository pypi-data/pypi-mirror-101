import setuptools
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="starform",
    version="0.0.1",
    author="Tommy Dong",
    author_email="tommydong1998@gmail.com",
    description="StarForm is a Python library to quickly develop clean modular models/pipelines.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TommyDong1998/StarFormation",
    packages=['starform','starform.classic'],
    install_requires=['pathos']
)