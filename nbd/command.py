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
