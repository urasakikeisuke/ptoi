"""setup.py"""

import setuptools  # type: ignore

with open("README.md", "r") as f:
    long_description = f.read()

DESCRIPTION = "Let's put text on it"
NAME = "ptoi"
AUTHOR = "urasakikeisuke"
AUTHOR_EMAIL = "urasakikeisuke.ml@gmail.com"
LICENSE = "MIT License"
VERSION = "1.2"
PYTHON_REQUIRES = ">=3.6"
INSTALL_REQUIRES = [
    "numpy",
    "pillow",
    "matplotlib",
    "wget",
]
PACKAGES = setuptools.find_packages()

setuptools.setup(
    name=NAME,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=AUTHOR,
    maintainer_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=long_description,
    license=LICENSE,
    version=VERSION,
    python_requires=PYTHON_REQUIRES,
    install_requires=INSTALL_REQUIRES,
    packages=PACKAGES,
)
