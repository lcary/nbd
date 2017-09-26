#!/bin/sh

set -e

python setup.py sdist
python setup.py bdist
python setup.py bdist_egg
