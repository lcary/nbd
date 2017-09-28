#!/bin/sh

set -euxo pipefail

cd $(git rev-parse --show-toplevel)

# clean
rm -rf dist/ build/
pip uninstall -y nbd || echo "Already uninstalled"

# build
python setup.py sdist

pip install ./dist/nbd-*.tar.gz

nbd demo/demo.ipynb
