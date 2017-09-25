#!/bin/python

import argparse
import distutils
import subprocess

DEFAULT_OUTPUT_DIR = 'ipynb_generated'


def mkdir_p(path):
  distutils.dir_util.mkpath(path)


class Convertor(object):

  def __init__(self, ipynb_path, output_dir):
    self.ipynb_path = ipynb_path
    self.output_dir = output_dir
    mkdir_p(output_dir)

  class NotebookConversionFailure(Exception):
    pass

  def _nbconvert(self, fmt):
    return subprocess.check_output([
      'jupyter',
      'nbconvert',
      self.ipynb_path,
      '--output-dir=',
      self.output_dir,
      '--to',
      fmt])

  def to_python(self):
    return self._nbconvert('python')

  def to_rst(self):
    return self._nbconvert('rst')

  def convert(self):
    self.to_python()
    self.to_rst()


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('ipynb_path', required=True)
  parser.add_argument('--output_dir', default=DEFAULT_OUTPUT_DIR)
  args = parser.parse_args()

  Convertor(args.ipynb_path, args.output_dir)

if __name__ == '__main__':
  main()
