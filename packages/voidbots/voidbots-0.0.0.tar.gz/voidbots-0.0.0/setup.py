from setuptools import setup
import setuptools
from distutils.core import setup

with open("README.md", "r", encoding="utf-8") as r:
    long_description = r.read()

setup(
    name="voidbots",
    license='MIT',
    author='sldless',
    description="VoidBots api but in python -_-",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=['requests'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
