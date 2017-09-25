#!/bin/python

from argparse import ArgumentParser
from distutils import dir_util
import logging
from os import path as ospath

from .command import cd_repo_root
from .convert import Converter

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

PKG_NAME = 'ipynb_diff'


def _log_setup(log_dir):
  # log setup
  formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

  # output to file
  log_file = '{}.log'.format(PKG_NAME)
  fh = logging.FileHandler(ospath.join(log_dir, log_file))
  fh.setLevel(logging.DEBUG)
  fh.setFormatter(formatter)
  logger.addHandler(fh)

  # output to console
  ch = logging.StreamHandler()
  ch.setLevel(logging.INFO)
  ch.setFormatter(formatter)
  logger.addHandler(ch)


def main():
  parser = ArgumentParser()
  parser.add_argument('files', nargs='+')
  parser.add_argument('--output_dir', default='ipynb_generated')
  args = parser.parse_args()

  # convert input paths to absolute paths
  path_dict = map(ospath.abspath, args.files)
  output_dir = ospath.abspath(args.output_dir)

  # create output dir for generated code
  dir_util.mkpath(output_dir)

  _log_setup(output_dir)

  # cd to the root of the git repo and convert files
  with cd_repo_root() as repo_root:
    Converter(path_dict, output_dir, repo_root).convert()

if __name__ == '__main__':
  main()
