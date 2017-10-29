import subprocess

from nbd.command import (ANSI_LIGHT_RED, echo)

HEAD = 'HEAD'

DEFAULT_ENCODING = 'utf-8'

class Git(object):
  """
  Namespace for git functions.
  """

  def __init__(self):
    # this should become a filesystem path if the need to specify
    # an absolute path to a user's git binary ever arises:
    self._git = 'git'

  def rev_parse_show_toplevel(self):
    args = [self._git, 'rev-parse', '--show-toplevel']
    echo(self._git, ANSI_LIGHT_RED, " ".join(args))
    output = subprocess.check_output(args)
    decoded = output.decode(DEFAULT_ENCODING)
    return decoded.strip('\n')

  def show(self, filepath, commit=HEAD):
    args = [self._git, 'show', '{}:{}'.format(commit, filepath)]
    echo(self._git, ANSI_LIGHT_RED, " ".join(args))
    return subprocess.check_output(args)

  def diff_no_index(self, file_a, file_b, options=None):
    args = [
      self._git,
      '--no-pager',
      'diff',
      '--exit-code',
      '--no-index',
      '--color=always']
    if options is not None:
      args.extend(options)
    args.extend([file_a, file_b])
    echo(self._git, ANSI_LIGHT_RED, " ".join(args))
    subprocess.call(args)

  def diff_name_status(self, commit):
    args = [self._git, 'diff', commit, '--name-status']
    echo(self._git, ANSI_LIGHT_RED, " ".join(args))
    return subprocess.check_output(args)
