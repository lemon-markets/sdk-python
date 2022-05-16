import os
from distutils.core import setup

from pkg_resources import parse_requirements
from setuptools import find_packages

version_content = {}
with open(os.path.join("lemon", "version.py"), encoding="utf-8") as f:
    exec(f.read(), version_content)

version = version_content["VERSION"]

setup(
    name="lemon",
    version=version,
    description="Official Python client for lemon.markets API",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    author="lemon.markets",
    author_email="support@lemon.markets",
    url="https://github.com/lemon-markets/sdk-python/",
    download_url="https://pypi.python.org/pypi/lemon/",
    project_urls={
        "Source": "https://github.com/lemon-markets/sdk-python/",
        "Changes": "https://github.com/lemon-markets/sdk-python/blob/master/CHANGELOG.md",
        "Tracker": "https://github.com/lemon-markets/sdk-python/issues/",
        "lemon.markets": "https://www.lemon.markets/",
        "API Documentation": "https://docs.lemon.markets/",
    },
    packages=find_packages(include=["lemon", "lemon.*"]),
    install_requires=parse_requirements("requirements.txt"),
    python_requires=">=3.7",
)
