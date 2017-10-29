#!/bin/python

import io
import os
import re
from subprocess import CalledProcessError, check_call, check_output

# before anything else, cd to repo root
repo_root = check_output('git rev-parse --show-toplevel', shell=True)
repo_root = repo_root.strip()
os.chdir(repo_root)


def shell(cmd):
  check_call(cmd, shell=True)


def read_from_root(*names, **kwargs):
  with io.open(
    os.path.join(repo_root.decode(), *names),
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


# clean
shell('rm -rf dist/ build/')

try:
  shell('pip uninstall -y nbd')
except CalledProcessError:
  print("Already uninstalled")

# build
shell('python setup.py bdist')
shell('python setup.py sdist')

version = find_version("nbd", "__init__.py")
shell('pip install ./dist/nbd-{}.tar.gz'.format(version))
