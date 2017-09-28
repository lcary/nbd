#!/bin/python

from argparse import (ArgumentParser, ArgumentDefaultsHelpFormatter)
import logging
from os import getcwd
from os import path as ospath

from .command import cd_if_necessary
from .const import PKG_NAME
from .diff import DiffGenerator
from .export import NotebookExporter
from .fileops import normrelpath
from .git import (Git, HEAD)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def _get_args():
  desc = 'The lightweight ipython notebook diffing tool'
  parser = ArgumentParser(
    description=desc,
    formatter_class=ArgumentDefaultsHelpFormatter)
  parser.add_argument(
    'notebooks',
    nargs='+',
    help='filepath(s) to ipython/jupyter notebooks')
  parser.add_argument(
    '-d',
    '--debug',
    action='store_true',
    help='display all log messages for debugging purposes')
  parser.add_argument(
    '-l',
    '--log-to-disk',
    action='store_true',
    help='output logs to filesystem')
  parser.add_argument(
    '--log-dir',
    default=getcwd(),
    help='specify log directory if logging to disk')
  parser.add_argument(
    '-v',
    '--nbformat-version',
    type=int,
    default=4,
    help='ipython/jupyter notebook format version')
  parser.add_argument(
    '-e',
    '--export-formats',
    action='append',
    choices=NotebookExporter.DEFAULT_EXPORT_FORMATS,
    help='only export specific formats. omit to export all formats.')
  parser.add_argument(
    '--old-commit',
    default=HEAD,
    help='earlier commit hash to diff against')
  parser.add_argument(
    '--new-commit',
    default=None,
    help='newer commit hash to diff against')
  parser.add_argument(
    '-g',
    '--git-diff-options',
    action='append',
    help='additional options to pass to git-diff')
  return parser.parse_args()


def _log_setup(debug_mode, log_dir, log_to_disk):
  # standard log format
  fmt = '%(asctime)s - %(levelname)s - %(message)s'
  formatter = logging.Formatter(fmt)

  if debug_mode:
    level = logging.DEBUG 
  else:
    level = logging.INFO

  if log_to_disk:
    # output logging to file
    log_file = '{}.log'.format(PKG_NAME)
    fh = logging.FileHandler(ospath.join(log_dir, log_file))
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
  _log_setup(args.debug, args.log_dir, args.log_to_disk)

  # convert input paths to absolute paths
  nb_filepaths = map(ospath.abspath, args.notebooks)

  # cd to the root of the git repo
  repo_root = Git.rev_parse_show_toplevel()
  with cd_if_necessary(repo_root):

    # relativize absolute filepaths to root of repo
    nb_filepaths = [normrelpath(fp, repo_root) for fp in nb_filepaths]

    # export notebooks to various git-diff-friendly formats in tempdir
    diff_gen = DiffGenerator(
      nb_filepaths,
      args.old_commit,
      args.new_commit,
      args.export_formats)
    diff_gen.get_diff(args.nbformat_version, args.git_diff_options)

if __name__ == '__main__':
  main()
