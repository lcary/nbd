#!/bin/python

from argparse import (ArgumentParser, ArgumentDefaultsHelpFormatter)
from distutils import dir_util
import logging
from os import path as ospath

from .command import (cd_if_necessary, git_repo_root)
from .const import PKG_NAME
from .diff import DiffGenerator
from .export import NotebookExporter
from .fileops import normrelpath

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def _get_args():
  desc = 'The lightweight ipython notebook diffing tool.'
  parser = ArgumentParser(
    description=desc,
    formatter_class=ArgumentDefaultsHelpFormatter)
  parser.add_argument(
    'notebooks',
    help='filepath(s) to ipython/jupyter notebooks',
    nargs='+')
  # change output dir if -d mode. doesn't make sense now.
  parser.add_argument(
    '-o',
    '--output-dir',
    help='output directory for exported files',
    default='nbd_generated')
  parser.add_argument(
    '-f',
    '--nbformat-version',
    help='ipython/jupyter notebook format version',
    default=4,
    type=int)
  parser.add_argument(
    '-e',
    '--export-to-repo',
    help='export data from notebooks into the output directory',
    action='store_true')
  # TODO: allow user to configure which commits to diff against via argparse subparser
  # TODO: add options to configure export formats
  # TODO: make disk logging optional, with log_dir set by user
  # TODO: allow user to set set log level
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
  nb_filepaths = map(ospath.abspath, args.notebooks)
  output_dir = ospath.abspath(args.output_dir)

  # create output dir and set as log dir
  dir_util.mkpath(output_dir)
  _log_setup(output_dir)

  # cd to the root of the git repo
  repo_root = git_repo_root()
  with cd_if_necessary(repo_root):

    # relativize absolute filepaths to root of repo
    output_dir = normrelpath(output_dir, repo_root)
    nb_filepaths = [normrelpath(fp, repo_root) for fp in nb_filepaths]

    if args.export_to_repo:
      # export notebooks to various git-diff-friendly formats in repo
      exporter = NotebookExporter(output_dir)
      exporter.setup()
      exporter.process_notebooks(nb_filepaths, args.nbformat_version)
      exporter.teardown()
    else:
      # export notebooks to various git-diff-friendly formats in tempdir
      diff_gen = DiffGenerator(nb_filepaths, "old_commit_sha", "new_commit_sha")
      diff_gen.get_diff(args.nbformat_version)

if __name__ == '__main__':
  main()
