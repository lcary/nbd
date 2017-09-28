from distutils import dir_util
from os import path as ospath

from .command import (git_diff_no_index, git_show_old_copy)
from .export import NotebookExporter
from .fileops import (get_file_id, mktempdir, write_file)


class DiffGenerator(object):

  def __init__(self, filepaths, old_commit_sha, new_commit_sha):
    self.filepaths = filepaths
    self.old_commit_sha = old_commit_sha
    self.new_commit_sha = new_commit_sha

  def _write_old_copy(self, filepath, output_dir):
    content = git_show_old_copy(filepath)
    filename = ospath.basename(filepath)
    write_file(output_dir, filename, content)
    return ospath.join(output_dir, filename)

  def _export_old_and_new_notebooks(self, tempdir, old_dir, new_dir, nbformat_version):
    for new_copy_filepath in self.filepaths:
      file_id = get_file_id(new_copy_filepath)
      # get previous copy of notebook from git history, output to tempdir
      old_copy_filepath = self._write_old_copy(new_copy_filepath, tempdir)
      # export data from old notebooks in tempdir
      exporter = NotebookExporter(old_dir)
      exporter.process_notebook(file_id, old_copy_filepath, nbformat_version)
      # export data from new notebooks in git repo
      exporter = NotebookExporter(new_dir)
      exporter.process_notebook(file_id, new_copy_filepath, nbformat_version)

  def get_diff(self, nbformat_version):
    with mktempdir() as tempdir:
      old_dir = ospath.join(tempdir, 'old')
      new_dir = ospath.join(tempdir, 'new')
      dir_util.mkpath(old_dir)
      dir_util.mkpath(new_dir)
      # # export data from notebooks in git repo and notebooks in tempdir
      self._export_old_and_new_notebooks(tempdir, old_dir, new_dir, nbformat_version)
      # show git diff of exported data within tempdir
      git_diff_no_index(old_dir, new_dir)
