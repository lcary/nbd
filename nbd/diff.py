from distutils import dir_util
from os import path as ospath

from .command import (ANSI_LIGHT_GREEN, echo)
from .const import PKG_NAME
from .export import NotebookExporter
from .fileops import (get_file_id, mktempdir, write_file)
from .git import Git


class DiffGenerator(object):

  def __init__(self, filepaths, old_commit, new_commit, export_formats):
    self.filepaths = filepaths
    # use these at some point
    self.old_commit = old_commit
    self.new_commit = new_commit
    self.export_formats = export_formats

  def _write_previous_version(self, filepath, output_dir, commit):
    """
    Write a committed version of a file to a given output directory.
    """
    content = Git.show(filepath, commit=commit)
    filename = ospath.basename(filepath)
    write_file(output_dir, filename, content)
    return ospath.join(output_dir, filename)

  def _export_old_and_new_notebooks(self, tempdir, old_dir, new_dir, nbformat_version):
    for filepath in self.filepaths:
      file_id = get_file_id(filepath)

      # get previous version of notebook from git history, output to tempdir
      old_filepath = self._write_previous_version(filepath, tempdir, self.old_commit)

      # get new version from git history if and only if a different commit
      # is requested. otherwise, get it directly from the filepath in repo.
      if self.new_commit is None:
        new_filepath = filepath
      else:
        new_filepath = self._write_previous_version(filepath, tempdir, self.new_commit)

      exporter = NotebookExporter(old_dir, self.export_formats)
      exporter.process_notebook(file_id, old_filepath, nbformat_version)
      exporter = NotebookExporter(new_dir, self.export_formats)
      exporter.process_notebook(file_id, new_filepath, nbformat_version)

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
