#!/bin/sh

set -euxo pipefail

cd $(git rev-parse --show-toplevel)

# clean
rm -rf dist/ build/
pip uninstall -y nbcrack || echo "Already uninstalled"

# build
python setup.py sdist

pip install ./dist/nbcrack-*.tar.gz

nbcrack example/def_wikipedia_visualization.ipynb
