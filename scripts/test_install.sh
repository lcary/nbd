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

# TODO: automatically parse __version__ like setup.py, this is a PITA.
#       this todo likely requires converting this to a python script.
pip install ./dist/nbd-0.1.*.tar.gz
