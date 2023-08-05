from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='NASApi',
    version='0.0.5',
    description="Simple NASA API wrapper",
    author='SleepingStar',
    author_email='mattisverytoxic@gmail.com',
    packages=['NASApi'],
    install_requires=['requests'],
    url='https://github.com/SleepingStar/NASApi',
    keywords='python NASA py',
    long_description=long_description,
    long_description_content_type='text/markdown'
)
