#!/bin/bash

set -e

# readme changes can be validated with restview
# discovered via https://github.com/pypa/pypi-legacy/issues/527#issuecomment-305822702
restview --pypi --long
