from setuptools import setup
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="tiny_net",
    version = "1.0.2",
    description="This library creates shorturl",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Sudhanshu Kumar",
    author_email="ksudhanshu961@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=['tinynet'],
    include_package_data=True,
    install_requires=["urllib3"]
)
