from contextlib import contextmanager
from os import path as ospath
from subprocess import CalledProcessError

from .context import (diff, git)
from .util import mock_write_file

from mock import (MagicMock, mock_open, patch)
import pytest

OLD_TEST_FILE = 'file_v2.ipynb'
NEW_TEST_FILE = 'file_v3.ipynb'


# ----------------------------- Test Fixtures ----------------------------


@pytest.fixture
def git_cmd():
  return git.Git()


@pytest.fixture
def diff_rename_line():
  return 'R100\t{}\t{}'.format(OLD_TEST_FILE, NEW_TEST_FILE)


@pytest.fixture
def diff_output(diff_rename_line):
  return (
    '{}\n'
    'M       nbd/diff.py\n'
    'M       nbd/tests/test_diff.py'.format(diff_rename_line))


@pytest.fixture
def diff_parser(git_cmd):
  return diff.GitDiffParser(git_cmd)


@pytest.fixture
def diff_generator(git_cmd):
  filepaths = ['foo']
  old_commit = 'd2eb065'
  new_commit = 'd760387'
  exporter = MagicMock()
  return diff.DiffGenerator(git_cmd, filepaths, old_commit, new_commit, exporter)


@pytest.fixture
def file_data():
  return diff.FileData('d2eb065', '/fake/tempdir', NEW_TEST_FILE, '/fake/output_dir')


# ------------------------------ Test Cases ------------------------------


def test_parse_previous_filename(diff_parser, diff_rename_line):
  old_filepath = diff_parser._parse_previous_filename(diff_rename_line, NEW_TEST_FILE)
  assert old_filepath == OLD_TEST_FILE


def test_parse_no_previous_filename(diff_parser, diff_rename_line):
  old_filepath = diff_parser._parse_previous_filename(diff_rename_line, 'some/other/file')
  assert old_filepath is None


def test_git_diff_renamed_files(diff_parser, diff_rename_line, diff_output):
  with patch('nbd.git.subprocess.check_output') as mock_check_output:
    mock_check_output.return_value = diff_output
    assert diff_parser._git_diff_renamed_files('f9574b6') == [diff_rename_line]


def test_retreive_renamed_file(diff_parser, file_data):
  with patch('nbd.git.subprocess.check_output') as mock_check_output:
    rename_line = 'R100\t{}\t{}\n'.format(OLD_TEST_FILE, file_data.input_filepath)
    mock_check_output.return_value = rename_line
    assert diff_parser.retreive_renamed_file(file_data) == OLD_TEST_FILE


def test_no_retreive_renamed_file(diff_parser, file_data):
  with patch('nbd.git.subprocess.check_output') as mock_check_output:
    mock_check_output.return_value = 'R100\t{}\tOTHERFILE!\n'.format(OLD_TEST_FILE)
    with pytest.raises(diff_parser.RenamedFileNotFound):
      diff_parser.retreive_renamed_file(file_data)


@contextmanager
def mock_git_and_check_output(side_effects, input_filepath, output_filepath):
  m = mock_open()
  test_file_content = '<some fake content>'

  try:
    with mock_write_file(m):
      with patch('nbd.git.subprocess.check_output') as mock_check_output:
        # test file content is always returned by git-show which runs last:
        mock_check_output.side_effect = side_effects + [test_file_content]
        yield
  finally:
    # assert output file was written with test file content
    m.assert_called_once_with(output_filepath, 'w')
    handle = m()
    handle.write.assert_called_once_with(test_file_content)


def test_try_write_renamed_file(diff_generator, file_data):
  input_filepath = file_data.input_filepath
  output_filename = 'Arbitrary Filename 1'
  output_filepath = ospath.join(file_data.tempdir, output_filename)
  side_effects = ['R100\t{}\t{}\n'.format(output_filename, input_filepath)]
  with mock_git_and_check_output(side_effects, input_filepath, output_filepath):
    diff_generator._try_write_renamed_file(file_data)


def test_write_previous_version_success(diff_generator, file_data):
  input_filepath = file_data.input_filepath
  output_filepath = ospath.join(file_data.tempdir, file_data.input_filepath)
  with mock_git_and_check_output([], input_filepath, output_filepath):
    assert diff_generator._write_previous_version(file_data) == output_filepath


def test_write_previous_version_fallback(diff_generator, file_data):
  input_filepath = file_data.input_filepath
  output_filename = 'Arbitrary Filename 2'
  output_filepath = ospath.join(file_data.tempdir, output_filename)
  side_effects = [
    CalledProcessError(diff.EXIT_CODE_128_FILE_NOT_FOUND, 'foo'),  # git-show
    'R100\t{}\t{}\n'.format(output_filename, input_filepath)]  # git-diff
  with mock_git_and_check_output(side_effects, input_filepath, output_filepath):
    assert diff_generator._write_previous_version(file_data) == output_filepath


def test_write_previous_version_failure(diff_generator, file_data):
  with mock_write_file(mock_open()):
    with patch('nbd.git.subprocess.check_output') as mock_check_output:
      # unknown error returned for the first git-show causes a top-level exception
      mock_check_output.side_effect = [CalledProcessError(5000000, 'unknown error')]
      with pytest.raises(CalledProcessError):
        diff_generator._write_previous_version(file_data)


def test_get_diff(diff_generator, file_data):
  m = mock_open()

  # mock all file system operations to ensure test is self-contained
  with mock_write_file(m):
    with patch('nbd.diff.dir_util.mkpath'):
      with patch('nbd.fileops.tempfile.mkdtemp') as mock_mkdtemp:
        mock_mkdtemp.return_value = file_data.tempdir
        with patch('nbd.fileops.shutil.rmtree'):
          with patch('nbd.git.subprocess.call') as mock_call:
            diff_generator.get_diff([])
            print mock_call.mock_calls
            mock_call.assert_called_once_with([
              'git',
              '--no-pager',
              'diff',
              '--exit-code',
              '--no-index',
              '--color=always',
              ospath.join(file_data.tempdir, 'old'),
              ospath.join(file_data.tempdir, 'new')])
