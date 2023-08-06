from setuptools import setup
import os

VERSION = "0.1.4"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="flake8-pathlib",
    description="flake8-pathlib is now flake8-use-pathlib",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    version=VERSION,
    install_requires=["flake8-use-pathlib"],
    classifiers=["Development Status :: 7 - Inactive"],
)
