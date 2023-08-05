import pathlib
from setuptools import setup, find_packages

package = find_packages()

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="tatumpython",
    version="1.0.0",
    description="tatum services",
    long_description=README,
    long_description_content_type="text/markdown",
    url="",
    author="Narasimha Sai",
    author_email="anarasimhasai24@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages= package,
    include_package_data=True,
    install_requires=['web3','cerberus','termcolor','requests','python-dotenv','bip32','bip-utils','pywallet','bip32utils','base58','mnemonic'],
)