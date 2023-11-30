"""The python wrapper for IQ Option API package setup."""
from setuptools import (setup, find_packages)
from iqoptionapi.version_control import api_version

setup(
    name="iqoptionapi",
    version=api_version,
    packages=find_packages(),
    install_requires=["pylint", "requests"],
    include_package_data=True,
    description="Best IQ Option API for python",
    long_description="Best IQ Option API for python",
    url="https://github.com/thiago95macedo/iqoptionapi",
    author="Thiago Macêdo",
    zip_safe=False
)
