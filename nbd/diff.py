from collections import namedtuple
from distutils import dir_util
import logging
from os import path as ospath
from subprocess import CalledProcessError

from nbd.command import (ANSI_LIGHT_GREEN, ANSI_LIGHT_RED, echo)
from nbd.const import PKG_NAME
from nbd.fileops import (get_file_id, mktempdir, write_file)

logger = logging.getLogger()

FileData = namedtuple('FileData', 'commit output_dir input_filepath tempdir')

EXIT_CODE_128_FILE_NOT_FOUND = 128


class DiffGenerator(object):

  def __init__(self, git_cmd, filepaths, old_commit, new_commit, exporter):
    self._git_cmd = git_cmd
    self._filepaths = filepaths
    self._old_commit = old_commit
    self._new_commit = new_commit
    self._parser = GitDiffParser(git_cmd)
    self.exporter = exporter

  def _write_renamed_file(self, file_data):
    """
    Write the contents of the file before it was renamed.
    Return the path the newly written file in the tempdir.
    """
    old_filepath = self._parser.retreive_renamed_file(file_data)
    content = self._git_cmd.show(old_filepath, commit=file_data.commit)
    filepath = ospath.join(file_data.tempdir, ospath.basename(old_filepath))
    write_file(filepath, content)
    return filepath

  def _try_write_renamed_file(self, file_data):
    """
    This fallback method checks if a file was renamed in git history.
    If it was renamed, this function writes content and returns the
    filepath to the old version of the file written to tempdir.
    Otherwise, it returns None to signify the file was not found.
    """
    try:
      return self._write_renamed_file(file_data)
    except (CalledProcessError, self._parser.RenamedFileNotFound):
      return None

  def _write_previous_version(self, file_data):
    """
    Write a committed version of a file to tempdir.
    """
    filename = ospath.basename(file_data.input_filepath)
    output_filepath = ospath.join(file_data.tempdir, filename)

    try:
      # If git shows the file at the input path, then we assume it was not renamed
      content = self._git_cmd.show(file_data.input_filepath, commit=file_data.commit)
    except CalledProcessError as exc:
      if exc.returncode == EXIT_CODE_128_FILE_NOT_FOUND:
        # The file does not exist in git history, indicated by the above exit code.
        # In this case, search git history to see if the file was renamed:
        return self._try_write_renamed_file(file_data)
      else:
        raise exc
    else:
      write_file(ospath.join(file_data.tempdir, filename), content, write_mode='wb')
      return output_filepath

  def _export_notebook_to_tempdir(self, file_id, file_data):
    """
    Export data from the notebook to a temporary directory.
    """

    if file_data.commit is None:
      # retrieve notebook from the input filepath.
      output_filepath = file_data.input_filepath
    else:
      # retrieve notebook from git history.
      output_filepath = self._write_previous_version(file_data)
    if output_filepath is not None:
      self.exporter.process_notebook(file_id, output_filepath, file_data.output_dir)

  def _export_old_and_new_notebooks(self, tempdir, old_dir, new_dir):
    for filepath in self._filepaths:
      file_id = get_file_id(filepath)
      old_file_data = FileData(self._old_commit, old_dir, filepath, tempdir)
      new_file_data = FileData(self._new_commit, new_dir, filepath, tempdir)
      self._export_notebook_to_tempdir(file_id, old_file_data)
      self._export_notebook_to_tempdir(file_id, new_file_data)


  def get_diff(self, git_diff_options):
    with mktempdir() as tempdir:
      # create old and new directories
      old_dir = ospath.join(tempdir, 'old')
      new_dir = ospath.join(tempdir, 'new')
      dir_util.mkpath(old_dir)
      dir_util.mkpath(new_dir)

      # # export data from notebooks in git repo and notebooks in tempdir
      self._export_old_and_new_notebooks(tempdir, old_dir, new_dir)

      # show git diff of exported data within tempdir
      msg = "git diff output below (no output == no diff)"
      echo(PKG_NAME, ANSI_LIGHT_GREEN, msg)
      self._git_cmd.diff_no_index(old_dir, new_dir, options=git_diff_options)


class GitDiffParser(object):
  """
  Fallback handler that retreives renamed filenames from git history.
  Things get ugly here. This class parses git diff output.

  The `git diff --name-status` command produces output like:

      R100\tdemo/demo2.ipynb\tdemo/demo3.ipynb

  Where the symbols are as follows:

      R             status indicating rename
      100           similarity index
      \t            delineator
      demo2.ipynb   old filename
      demo3.ipynb   new filename

  If a renamed file cannot be found, an exception is raised.
  """

  def __init__(self, git_cmd):
    self._git_cmd = git_cmd

  class RenamedFileNotFound(Exception):
    """
    Raise when unable to find renamed files in git-diff output.
    """
    pass

  @staticmethod
  def _parse_previous_filename(rename_line, input_filepath):
    try:
      (status, old_filepath, new_filepath) = rename_line.split('\t')
    except ValueError as e:
      logger.warn('Unable to parse git output: {}'.format(rename_line))
      logger.debug(str(e))
    else:
      if new_filepath.strip() == input_filepath:
        return old_filepath
    return None

  def _git_diff_renamed_files(self, commit):
    """
    This function runs the git-diff command and returns rename lines.
    """
    output = self._git_cmd.diff_name_status(commit)
    lines = output.split('\n')
    return [l for l in lines if l.startswith('R')]

  def retreive_renamed_file(self, file_data):
    """
    Return the filepath of the previous filename if it was renamed.
    Otherwise, throw exception.
    """
    input_filepath = file_data.input_filepath
    renamed_file_lines = self._git_diff_renamed_files(file_data.commit)

    for line in renamed_file_lines:
      old_filepath = self._parse_previous_filename(line, input_filepath)
      if old_filepath is not None:
        msg = 'git shows renamed file:\n{}'.format(line)
        echo('git', ANSI_LIGHT_RED, msg, lvl=logger.info)
        return old_filepath

    msg = 'Unable to detect renamed version of file: {}'.format(input_filepath)
    raise self.RenamedFileNotFound(msg)
