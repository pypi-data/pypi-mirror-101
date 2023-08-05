from setuptools import setup
from os import path


# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
dirx = this_directory + "/ppski_distributions"
with open(path.join(dirx, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="ppski_distributions",
    version="0.2",
    description="Gaussian and Binomial distributions",
    packages=["ppski_distributions"],
    author="Paula Pawlowski",
    author_email="paula.pwski@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    zip_safe=False,
)
