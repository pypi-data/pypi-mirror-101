import pathlib
from setuptools import setup

# Directory of this file
HERE = pathlib.Path(__file__).parent

# Text of the README file
README = HERE.joinpath("README.md").read_text()

# This is the call which does all the work
setup(
    name="smartetailing",
    version="0.3.0",  # TODO - Match this to smartetailing/__init__.py
    description="Connect to the smart etailing website order feeds",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/fundthmcalculus/smartetailing",  # TODO - Create this repo
    author="Scott Phillips",
    author_email="phillips.scott@sandsas.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",  # TODO - Python 3.X?
    ],
    packages=["smartetailing"],
    include_package_data=True,
    install_requires=["lxml", "requests"],  # TODO - Pull from requirements.txt?

)