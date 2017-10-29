from .context import git

from mock import patch
import pytest


@pytest.fixture
def test_filepath():
  return "/path/to/git/repo/file.ipynb"


@pytest.fixture
def test_output():
  return "Foo\n"


@pytest.fixture
def git_cmd():
  return git.Git()


def test_git_rev_parse_show_toplevel(git_cmd, test_output):
  with patch('nbd.git.subprocess.check_output') as mock_check_output:
    mock_check_output.return_value = test_output.encode()
    assert git_cmd.rev_parse_show_toplevel() == test_output.strip()
    mock_check_output.assert_called_once()


def test_git_show(git_cmd, test_filepath, test_output):
  with patch('nbd.git.subprocess.check_output') as mock_check_output:
    mock_check_output.return_value = test_output
    assert git_cmd.show(test_filepath) == test_output
    mock_check_output.assert_called_once()


def test_git_diff_no_index(git_cmd, test_output):
  filepath1 = 'path/to/notebook1.ipynb'
  filepath2 = 'path/to/notebook2.ipynb'
  with patch('nbd.git.subprocess.call') as mock_call:
    git_cmd.diff_no_index(filepath1, filepath2)
    mock_call.assert_called_once()


def test_git_diff_name_status(git_cmd, test_filepath, test_output):
  with patch('nbd.git.subprocess.check_output') as mock_check_output:
    mock_check_output.return_value = test_output
    assert git_cmd.diff_name_status(test_filepath) == test_output
    mock_check_output.assert_called_once()
