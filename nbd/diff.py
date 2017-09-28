from distutils import dir_util
from os import path as ospath

from .command import (ANSI_LIGHT_GREEN, echo)
from .const import PKG_NAME
from .export import NotebookExporter
from .fileops import (get_file_id, mktempdir, write_file)
from .git import Git


class DiffGenerator(object):

  def __init__(self, notebook_filepaths, old_commit_sha, new_commit_sha):
    self.notebook_filepaths = notebook_filepaths
    # use these at some point
    self.old_commit_sha = old_commit_sha
    self.new_commit_sha = new_commit_sha

  def _write_old_copy(self, filepath, output_dir):
    content = Git.show_old_copy(filepath)
    filename = ospath.basename(filepath)
    write_file(output_dir, filename, content)
    return ospath.join(output_dir, filename)

  def _export_old_and_new_notebooks(self, tempdir, old_dir, new_dir, nbformat_version):
    for new_copy_filepath in self.notebook_filepaths:
      file_id = get_file_id(new_copy_filepath)
      # get previous copy of notebook from git history, output to tempdir
      old_copy_filepath = self._write_old_copy(new_copy_filepath, tempdir)
      # export data from old notebooks in tempdir
      exporter = NotebookExporter(old_dir)
      exporter.process_notebook(file_id, old_copy_filepath, nbformat_version)
      # export data from new notebooks in git repo
      exporter = NotebookExporter(new_dir)
      exporter.process_notebook(file_id, new_copy_filepath, nbformat_version)

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
