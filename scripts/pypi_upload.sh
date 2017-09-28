#!/bin/bash

set -e

# Tools that support PyPI.org by default are twine v1.8.0+ (recommended tool),
# setuptools 27+, or the distutils included with Python 3.4.6+, Python 3.5.3+,
# Python 3.6+, and 2.7.13+. e.g.:
# 
#     pip list | grep setuptools
#     setuptools (36.5.0)
# 
# from: https://packaging.python.org/guides/migrating-to-pypi-org/#uploading

python setup.py sdist upload
