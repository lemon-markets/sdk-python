from distutils.core import setup

from pkg_resources import parse_requirements
from setuptools import find_packages


def get_version():
    with open("lemonapi/__init__.py") as file:
        for line in file:
            if line.startswith("version"):
                return line.split('"')[1]


setup(
    name="lemonapi",
    version=get_version(),
    description="Official python sdk for lemon.markets",
    long_description=open("README.md").read(),
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
    # author="",
    # author_email="",
    url="https://github.com/lemon-markets/sdk-python/",
    download_url="https://pypi.python.org/pypi/lemonapi/",
    project_urls={
        "Source": "https://github.com/lemon-markets/sdk-python/",
        "Tracker": "https://github.com/lemon-markets/sdk-python/issues/",
        "lemon.markets": "https://www.lemon.markets/",
        "API Documentation": "https://docs.lemon.markets/",
    },
    packages=find_packages(include=["lemonapi", "lemonapi.*"]),
    install_requires=parse_requirements("requirements.txt"),
    python_requires=">=3.7",
)
