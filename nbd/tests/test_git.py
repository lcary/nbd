from .context import git

from mock import patch

def test_git_rev_parse_show_toplevel():
    git_cmd = git.Git()
    args = [git_cmd._git, 'rev-parse', '--show-toplevel']
    with patch('nbd.git.subprocess.check_output') as mock_check_output:
        mock_check_output.return_value = "Foo\n"
        assert git_cmd.rev_parse_show_toplevel() == "Foo"
        mock_check_output.assert_called_once_with(args)

def test_git_show():
    git_cmd = git.Git()
    filepath = 'path/to/myfile'
    args = [git_cmd._git, 'show', '{}:{}'.format(git.HEAD, filepath)]
    with patch('nbd.git.subprocess.check_output') as mock_check_output:
        mock_check_output.return_value = "Foo\n"
        assert git_cmd.show(filepath) == "Foo\n"
        mock_check_output.assert_called_once_with(args)

def test_git_diff_no_index():
    git_cmd = git.Git()
    filepath1 = 'path/to/myfile_1'
    filepath2 = 'path/to/myfile_2'

    args = [
        git_cmd._git,
        '--no-pager',
        'diff',
        '--exit-code',
        '--no-index',
        '--color=always',
        filepath1,
        filepath2]

    with patch('nbd.git.subprocess.call') as mock_call:
        git_cmd.diff_no_index(filepath1, filepath2)
        mock_call.assert_called_once_with(args)

def test_git_diff_name_status():
    git_cmd = git.Git()
    filepath = 'path/to/myfile'
    args = [git_cmd._git, 'diff', filepath, '--name-status']
    with patch('nbd.git.subprocess.check_output') as mock_check_output:
        mock_check_output.return_value = "Foo\n"
        assert git_cmd.diff_name_status(filepath) == "Foo\n"
        mock_check_output.assert_called_once_with(args)
