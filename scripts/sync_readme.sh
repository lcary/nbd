#!/bin/bash

set -e

# cd to repo root
cd "$( dirname "${BASH_SOURCE[0]}" )"
cd $(git rev-parse --show-toplevel)

# required to keep markdown readme in sync with rst for setuptools
pandoc --from=markdown --to=rst --output=README.rst README.md
