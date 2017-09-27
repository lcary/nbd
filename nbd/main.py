#!/bin/python

from argparse import ArgumentParser
from distutils import dir_util
import logging
from os import path as ospath

from .command import (cd_if_necessary, git_repo_root)
from .const import PKG_NAME
from .export import NotebookExporter
from .fileops import normrelpath

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def _get_args():
  desc = 'The lightweight ipython notebook diffing tool'
  parser = ArgumentParser(
    description=desc)
  parser.add_argument(
    'files',
    help='path(s) to ipython/jupyter notebooks',
    nargs='+')
  parser.add_argument(
    '--output-dir',
    help='output directory for exported files',
    default='nbd_generated')
  parser.add_argument(
    '--nbformat-version',
    default=4,
    type=int)
  return parser.parse_args()

def _log_setup(log_dir):
  # standard log format
  fmt = '%(asctime)s - %(levelname)s - %(message)s'
  formatter = logging.Formatter(fmt)

  # output logging to file
  log_file = '{}.log'.format(PKG_NAME)
  fh = logging.FileHandler(ospath.join(log_dir, log_file))
  fh.setLevel(logging.DEBUG)
  fh.setFormatter(formatter)
  logger.addHandler(fh)

  # output logging to console
  ch = logging.StreamHandler()
  ch.setLevel(logging.INFO)
  ch.setFormatter(formatter)
  logger.addHandler(ch)


def main():
  # commandline args
  args = _get_args()

  # convert input paths to absolute paths
  files = map(ospath.abspath, args.files)
  output_dir = ospath.abspath(args.output_dir)

  # create output dir and set as log dir
  dir_util.mkpath(output_dir)
  _log_setup(output_dir)

  # cd to the root of the git repo
  repo_root = git_repo_root()
  with cd_if_necessary(repo_root):

    # relativize absolute filepaths to root of repo
    output_dir = normrelpath(output_dir, repo_root)
    files = [normrelpath(fp, repo_root) for fp in files]

    exporter = NotebookExporter(output_dir)
    exporter.setup()
    exporter.process(files, args.nbformat_version)
    exporter.teardown()

if __name__ == '__main__':
  main()
