from subprocess import (call, check_output)

from .command import (ANSI_LIGHT_RED, echo)


class Git(object):
  """
  Namespace for git functions.
  """

  @staticmethod
  def rev_parse_show_toplevel():
    args = ['git', 'rev-parse', '--show-toplevel']
    echo('git', ANSI_LIGHT_RED, " ".join(args))
    return check_output(args).strip('\n')

  @staticmethod
  def show_old_copy(filepath, commit='HEAD'):
    args = ['git', 'show', '{}:{}'.format(commit, filepath)]
    echo('git', ANSI_LIGHT_RED, " ".join(args))
    return check_output(args)

  @staticmethod
  def diff_no_index(file_a, file_b, options=None):
    args = [
      'git',
      '--no-pager',
      'diff',
      '--exit-code',
      '--no-index',
      '--color=always']
    if options is not None:
      args.extend(options)
    args.extend([file_a, file_b])
    echo('git', ANSI_LIGHT_RED, " ".join(args))
    call(args)
