#!/bin/sh

set -euxo pipefail

# cd to repo root
cd "$( dirname "${BASH_SOURCE[0]}" )"
cd $(git rev-parse --show-toplevel)

# clean
rm -rf dist/ build/
pip uninstall -y nbd || echo "Already uninstalled"

# build
python setup.py bdist
python setup.py sdist

pip install ./dist/nbd-*.tar.gz
