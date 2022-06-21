import os
from distutils.core import setup

from setuptools import find_packages


def get_version():
    content = {}
    with open(os.path.join("lemon", "version.py"), encoding="utf-8") as f:
        exec(f.read(), content)
    return content["VERSION"]


def get_long_description():
    with open("README.md", "r") as fh:
        long_description = fh.read()

    long_description += "\n\n"

    with open("CHANGELOG.md", "r") as fh:
        long_description += fh.read()

    return long_description


def get_requirements():
    with open("requirements.txt", "r") as fh:
        requirements = fh.read().splitlines()
    return requirements


setup(
    name="lemon",
    version=get_version(),
    description="Official Python client for lemon.markets API",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="lemon.markets",
    author_email="support@lemon.markets",
    url="https://github.com/lemon-markets/sdk-python/",
    packages=find_packages(include=["lemon", "lemon.*"]),
    include_package_data=True,
    python_requires=">=3.7, <4",
    install_requires=get_requirements(),
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries",
    ],
    download_url="https://pypi.python.org/pypi/lemon/",
    project_urls={
        "Source": "https://github.com/lemon-markets/sdk-python/",
        "Changes": "https://github.com/lemon-markets/sdk-python/blob/master/CHANGELOG.md",
        "Tracker": "https://github.com/lemon-markets/sdk-python/issues/",
        "lemon.markets": "https://www.lemon.markets/",
        "API Documentation": "https://docs.lemon.markets/",
    },
)
