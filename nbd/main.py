#!/bin/python

from argparse import (ArgumentParser, ArgumentDefaultsHelpFormatter)
import logging
from os import path as ospath

from .command import (cd_if_necessary, git_repo_root)
from .const import PKG_NAME
from .diff import DiffGenerator
from .fileops import normrelpath

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def _get_args():
  desc = 'The lightweight ipython notebook diffing tool'
  parser = ArgumentParser(
    description=desc,
    formatter_class=ArgumentDefaultsHelpFormatter)
  parser.add_argument(
    'notebooks',
    help='filepath(s) to ipython/jupyter notebooks',
    nargs='+')
  parser.add_argument(
    '-d',
    '--debug',
    help='display all log messages for debugging purposes',
    action='store_true')
  parser.add_argument(
    '-l',
    '--log-to-disk',
    help='output {} logs to filesystem'.format(PKG_NAME),
    action='store_true')
  parser.add_argument(
    '-f',
    '--nbformat-version',
    help='ipython/jupyter notebook format version',
    default=4,
    type=int)
  # TODO: allow user to configure which commits to diff against via argparse subparser
  # TODO: add options to configure export formats
  parser.add_argument(
    '-g',
    '--git-diff-options',
    help='additional options to pass to git-diff',
    action='append')
  return parser.parse_args()


def _log_setup(debug, log_to_disk):
  # standard log format
  fmt = '%(asctime)s - %(levelname)s - %(message)s'
  formatter = logging.Formatter(fmt)

  if debug:
    level = logging.DEBUG 
  else:
    level = logging.INFO

  if log_to_disk:
    # output logging to file
    log_file = '{}.log'.format(PKG_NAME)
    fh = logging.FileHandler(log_file)
    fh.setLevel(level)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

  # output logging to console
  ch = logging.StreamHandler()
  ch.setLevel(level)
  ch.setFormatter(formatter)
  logger.addHandler(ch)


def main():
  # commandline args
  args = _get_args()
  _log_setup(args.debug, args.log_to_disk)

  # convert input paths to absolute paths
  nb_filepaths = map(ospath.abspath, args.notebooks)

  # cd to the root of the git repo
  repo_root = git_repo_root()
  with cd_if_necessary(repo_root):

    # relativize absolute filepaths to root of repo
    nb_filepaths = [normrelpath(fp, repo_root) for fp in nb_filepaths]

    # TODO: replace those fake shas!
    # export notebooks to various git-diff-friendly formats in tempdir
    diff_gen = DiffGenerator(nb_filepaths, "old_commit_sha", "new_commit_sha")
    diff_gen.get_diff(args.nbformat_version, args.git_diff_options)

if __name__ == '__main__':
  main()
