#!/bin/bash

set -e

# cd to repo root
cd "$( dirname "${BASH_SOURCE[0]}" )"
cd $(git rev-parse --show-toplevel)

perl -pi -e 's/2 \* np.pi/2.1 \* np.pi/g' demo/demo.ipynb
