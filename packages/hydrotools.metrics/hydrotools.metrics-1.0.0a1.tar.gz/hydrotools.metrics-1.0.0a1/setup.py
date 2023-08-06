#!/usr/bin/env python3
from setuptools import setup, find_namespace_packages

# python namespace subpackage
# this namespace package follows PEP420
# https://packaging.python.org/guides/packaging-namespace-packages/#native-namespace-packages

NAMESPACE_PACKAGE_NAME = "hydrotools"
SUBPACKAGE_NAME = "metrics"

# Namespace subpackage slug.
# Ex: mypkg.a # Where the namespace pkg = `mypkg` and the subpackage = `a`
SUBPACKAGE_SLUG = f"{NAMESPACE_PACKAGE_NAME}.{SUBPACKAGE_NAME}"

# Subpackage version
VERSION = "1.0.0-alpha.1"
URL = "https://github.com/NOAA-OWP/hydrotools"

# Package author information
AUTHOR = "Jason Regina"
AUTHOR_EMAIL = "jason.regina@noaa.gov"

# Short sub-package description
DESCRIPTION = "Variety of standard model evaluation metrics."

# Package dependency requirements
REQUIREMENTS = ["pandas", "numpy>=1.20.0"]

setup(
    name=SUBPACKAGE_SLUG,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    classifiers=[
        "",
    ],
    description=DESCRIPTION,
    namespace_packages=[NAMESPACE_PACKAGE_NAME],
    packages=find_namespace_packages(include=[f"{NAMESPACE_PACKAGE_NAME}.*"]),
    package_data={},
    install_requires=REQUIREMENTS,
)
