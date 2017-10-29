from .context import git

import pytest

@pytest.fixture
def command():
    class Command(object):
        def __init__(self):
            self.last_call = None
        def join(self, args):
            return ' '.join(args)
        def call(self, args):
            result = self.join(args)
            self.last_call = result
        def check_output(self, args):
            result = self.join(args)
            self.last_call = result
            return result
    return Command()

def test_git_rev_parse_show_toplevel(command):
    git_cmd = git.Git(command=command)
    expect = '{} rev-parse --show-toplevel'.format(git_cmd._git)
    assert git_cmd.rev_parse_show_toplevel() == expect

def test_git_show(command):
    git_cmd = git.Git(command=command)
    filepath = 'path/to/myfile'
    expect = '{} show {}:{}'.format(git_cmd._git, git.HEAD, filepath)
    assert git_cmd.show(filepath) == expect

def test_git_diff_no_index(command):
    git_cmd = git.Git(command=command)
    raw_str = '{} --no-pager diff --exit-code --no-index --color=always {} {}'
    filepath1 = 'path/to/myfile_1'
    filepath2 = 'path/to/myfile_2'
    expect = raw_str.format(git_cmd._git, filepath1, filepath2)
    git_cmd.diff_no_index(filepath1, filepath2)
    assert command.last_call == expect
    git_cmd.diff_no_index(filepath2, filepath1)
    assert command.last_call != expect

def test_git_diff_name_status(command):
    git_cmd = git.Git(command=command)
    filepath = 'path/to/myfile'
    expect = '{} diff {} --name-status'.format(git_cmd._git, filepath)
    assert git_cmd.diff_name_status(filepath) == expect
