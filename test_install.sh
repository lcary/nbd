#!/bin/sh

set -e

cd $(git rev-parse --show-toplevel)

# clean
rm -rf dist/ build/
pip uninstall -y nbexplode || echo "Already uninstalled"

# build
python setup.py sdist

pip install ./dist/nbexplode-*.tar.gz

nbexplode example/def_wikipedia_visualization.ipynb
