
import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="kdewallet",
    version="1.0.1",
    description="kdewallet interface",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/syntaxfiend/kdewallet",
    author="Connor Johnson",
    author_email="CONjamesNOR@gmail.com",
    license="GNU",
    classifiers=["Programming Language :: Python :: 3.8"],
    packages=find_packages(exclude=('tests',))
)
