#!/bin/python

import io
import os
import re
import setuptools
from subprocess import check_call, check_output
import sys

# before anything else, cd to repo root
repo_root = check_output('git rev-parse --show-toplevel', shell=True)
repo_root = repo_root.strip()
os.chdir(repo_root)


def shell(cmd):
    check_call(cmd, shell=True)


def read_from_root(*names, **kwargs):
    with io.open(
        os.path.join(repo_root, *names),
        encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read_from_root(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


class SetuptoolsTooOld(Exception):
    pass

# Tools that support PyPI.org by default are twine v1.8.0+ (recommended tool),
# setuptools 27+, or the distutils included with Python 3.4.6+, Python 3.5.3+,
# Python 3.6+, and 2.7.13+. e.g.:
# 
#     pip list | grep setuptools
#     setuptools (36.5.0)
# 
# from: https://packaging.python.org/guides/migrating-to-pypi-org/#uploading
if (sys.version_info[0] <= 2 and sys.version_info[1] <= 7 and sys.version_info[2] < 13):
    if int(setuptools.__version__.split('.')[0]) < 27:
        msg = (
            'The setuptools version should be 27+ when running anything less than '
            'python 2.7.13 but you are using setuptools version {}. upgrade it w/ pip.'
            ).format(setuptools.__version__)
        raise SetuptoolsTooOld(msg)


# upload to pypi
check_call('python setup.py sdist upload', shell=True)

# git tag
version = find_version('nbd', '__init__.py')
commit = check_output('git log -1 --format=%s', shell=True).strip()
check_call('git tag -a "v{}" -m "{}"'.format(version, commit), shell=True)
