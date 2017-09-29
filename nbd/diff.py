from distutils import dir_util
import logging
from os import path as ospath
from subprocess import CalledProcessError

from .command import (ANSI_LIGHT_GREEN, echo)
from .const import PKG_NAME
from .export import NotebookExporter
from .fileops import (get_file_id, mktempdir, write_file)
from .git import Git

logger = logging.getLogger()


class DiffGenerator(object):

  def __init__(self, filepaths, old_commit, new_commit, export_formats):
    self.filepaths = filepaths
    # use these at some point
    self.old_commit = old_commit
    self.new_commit = new_commit
    self.export_formats = export_formats

  class StillUnableToFindFile(Exception):
    pass

  @classmethod
  def _check_for_renamed_files_in_status(cls, filepath, commit):
    """
    This function tries to find renames and the commit of the rename
    for a given filepath. If we can find it, we can read the content 
    via git show later. Otherwise, raise an error.
    """
    output = Git.diff_name_status(commit)
    output_lines = output.split('\n')
    renames = [l for l in output_lines if l.startswith('R')]
    for rn_line in renames:
      try:
        (status, old_fp, new_fp) = rn_line.split('\t')
      except ValueError as e:
        logger.warn('Unable to parse git output: {}'.format(rn_line))
        logger.debug(str(e))
      else:
        if new_fp.strip() == filepath:
          echo('git', ANSI_LIGHT_GREEN, 'git shows renamed file:\n{}'.format(rn_line), lvl=logger.info)
          return old_fp
    raise cls.StillUnableToFindFile("Still can't find it!")

  @classmethod
  def _handle_file_not_found(cls, input_filepath, filename, output_filepath, output_dir, commit):
    try:
      old_fp = cls._check_for_renamed_files_in_status(input_filepath, commit)
      content = Git.show(old_fp, commit=commit)
      write_file(output_dir, filename, content)
      return output_filepath
    except (cls.StillUnableToFindFile, CalledProcessError):
      return None

  def _write_previous_version(self, input_filepath, output_dir, commit):
    """
    Write a committed version of a file to a given output directory.
    """
    filename = ospath.basename(input_filepath)
    output_filepath = ospath.join(output_dir, filename)
    try:
      content = Git.show(input_filepath, commit=commit)
    except CalledProcessError as e:
      if e.returncode == 128:
        return self._handle_file_not_found(
          input_filepath,
          filename,
          output_filepath,
          output_dir,
          commit)
      else:
        raise e
    else:
      write_file(output_dir, filename, content)
    # return the output filepath in all cases:
    return output_filepath

  def _export_old_and_new_notebooks(self, tempdir, old_dir, new_dir, nbformat_version):
    for relative_filepath in self.filepaths:
      file_id = get_file_id(relative_filepath)

      # TODO: this code is not very DRY

      # get new version of notebook from git history if and only if a different commit
      # is requested. otherwise, get it directly from the filepath in repo.
      if self.new_commit is None:
        new_filepath = relative_filepath
      else:
        new_filepath = self._write_previous_version(relative_filepath, tempdir, self.new_commit)

      if new_filepath is not None:
        exporter = NotebookExporter(new_dir, self.export_formats)
        exporter.process_notebook(file_id, new_filepath, nbformat_version)

      # get previous version of notebook from git history, output to tempdir
      old_filepath = self._write_previous_version(relative_filepath, tempdir, self.old_commit)

      if old_filepath is not None:
        exporter = NotebookExporter(old_dir, self.export_formats)
        exporter.process_notebook(file_id, old_filepath, nbformat_version)


  def get_diff(self, nbformat_version, git_diff_options):
    with mktempdir() as tempdir:
      old_dir = ospath.join(tempdir, 'old')
      new_dir = ospath.join(tempdir, 'new')
      dir_util.mkpath(old_dir)
      dir_util.mkpath(new_dir)
      # # export data from notebooks in git repo and notebooks in tempdir
      self._export_old_and_new_notebooks(tempdir, old_dir, new_dir, nbformat_version)
      # show git diff of exported data within tempdir
      msg = "git diff output below (no output == no diff)"
      echo(PKG_NAME, ANSI_LIGHT_GREEN, msg)
      Git.diff_no_index(old_dir, new_dir, options=git_diff_options)
