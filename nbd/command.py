from contextlib import contextmanager
import logging
from os import (chdir, getcwd)
from subprocess import (call, check_output)

logger = logging.getLogger()

ANSI_LIGHT_RED = 31
ANSI_LIGHT_GREEN = 32


def _color(msg, ansicode):
  return '\033[1;{ansicode};40m{msg}\033[0m'.format(msg=msg, ansicode=ansicode)


def echo(subject, ansicode, msg):
  logger.debug('{}: {}'.format(_color(subject, ansicode), msg))


def _cd_with_echo(path):
  echo('cd', ANSI_LIGHT_GREEN, path)
  chdir(path)


@contextmanager
def cd_if_necessary(path):
  orig = getcwd()
  should_cd = (orig != path)
  try:
    if should_cd:
      _cd_with_echo(path)
    yield
  finally:
    if should_cd:
      _cd_with_echo(orig)
    else:
      pass


def git_repo_root():
  args = ['git', 'rev-parse', '--show-toplevel']
  echo('git', ANSI_LIGHT_RED, " ".join(args))
  return check_output(args).strip('\n')


def git_show_old_copy(filepath, commit='HEAD^'):
  args = ['git', 'show', '{}:{}'.format(commit, filepath)]
  echo('git', ANSI_LIGHT_RED, " ".join(args))
  return check_output(args)


def git_diff_no_index(file_a, file_b, options=None):
  args = [
    'git',
    '--no-pager',
    'diff',
    '--exit-code',
    '--no-index',
    '--color=always',
    ]
  if options is not None:
    args.extend(options)
  args.extend([file_a, file_b])
  echo('git', ANSI_LIGHT_RED, " ".join(args))
  call(args)
