from contextlib import contextmanager
import logging
from os import (chdir, getcwd)
from subprocess import check_output

logger = logging.getLogger()

ANSI_LIGHT_RED = 31
ANSI_LIGHT_GREEN = 32


def _color(msg, ansicode):
  return '\033[1;{ansicode};40m{msg}\033[0m'.format(msg=msg, ansicode=ansicode)


def echo(subject, ansicode, msg):
  logger.info('{}: {}'.format(_color(subject, ansicode), msg))


class Command(object):

  @staticmethod
  def _echo(args):
    echo("running", ANSI_LIGHT_RED, " ".join(args))

  @classmethod
  def run(cls, args, echo=True):
    if echo:
      cls._echo(args)
    return check_output(args)


def _cd_with_echo(path):
  echo('cd', ANSI_LIGHT_GREEN, path)
  chdir(path)


@contextmanager
def _cd_if_necessary(path):
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


@contextmanager
def cd_repo_root():
  args = ['git', 'rev-parse', '--show-toplevel']
  repo_root = Command().run(args).strip('\n')
  try:
    with _cd_if_necessary(repo_root):
      yield repo_root
  finally:
    pass