#!/bin/bash

set -e

# cd to repo root
cd "$( dirname "${BASH_SOURCE[0]}" )"
cd $(git rev-parse --show-toplevel)

python -m nbd.main "$@"
