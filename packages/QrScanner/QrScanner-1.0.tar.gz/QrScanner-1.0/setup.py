import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="QrScanner",
    version="1.0",
    description="QrCode Scanner",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Rahul Shah",
    author_email="rahul.shah102006@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["QrScanner"],
    include_package_data=True,
    install_requires=['pyzbar','opencv-python'],
)
       
    
