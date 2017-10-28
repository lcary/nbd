from subprocess import (call, check_output)

from nbd.command import (ANSI_LIGHT_RED, echo)

HEAD = 'HEAD'

class Git(object):
  """
  Namespace for git functions.
  """

  # GIT should become an instance attribute if the need to specify
  # an absolute path to a user's git binary ever arises.
  GIT = 'git'

  @staticmethod
  def rev_parse_show_toplevel():
    args = [Git.GIT, 'rev-parse', '--show-toplevel']
    echo(Git.GIT, ANSI_LIGHT_RED, " ".join(args))
    return check_output(args).strip('\n')

  @staticmethod
  def show(filepath, commit=HEAD):
    args = [Git.GIT, 'show', '{}:{}'.format(commit, filepath)]
    echo(Git.GIT, ANSI_LIGHT_RED, " ".join(args))
    return check_output(args)

  @staticmethod
  def diff_no_index(file_a, file_b, options=None):
    args = [
      Git.GIT,
      '--no-pager',
      'diff',
      '--exit-code',
      '--no-index',
      '--color=always']
    if options is not None:
      args.extend(options)
    args.extend([file_a, file_b])
    echo(Git.GIT, ANSI_LIGHT_RED, " ".join(args))
    call(args)

  @staticmethod
  def diff_name_status(commit):
    args = [Git.GIT, 'diff', commit, '--name-status']
    echo(Git.GIT, ANSI_LIGHT_RED, " ".join(args))
    return check_output(args)
