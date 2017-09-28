from distutils import dir_util
from os import path as ospath
from subprocess import CalledProcessError

import nbformat as nbf

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

  def _write_empty_notebook(self, output_filepath):
    nb = nbf.v4.new_notebook()
    with open(output_filepath, 'w') as f:
      nbf.write(nb, f)
    return output_filepath

  class StillNoDice(Exception): pass

  def _check_if_renamed(self, filepath, commit):
    # this function should parse and run:
    #     git log --format='%H' --name-only --follow -- demo/demo.ipynb
    # to find renames and the commit of the rename for a given filepath.
    pass

  def _handle_git_show_128_error(self, input_filepath, filename, output_filepath, output_dir, commit):
    # this means the file exists on disk, but not in a previous commit.
    # In this case lets assume it's a new notebook file.
    # It's likely a bad assumtion in some cases, but hopefully not most.
    # TODO: handle file renames via self._check_if_renamed()
    # try:
    #   content = self._check_if_renamed(input_filepath, commit)
    #   write_file(output_dir, filename, content)
    #   return output_filepath
    # except self.StillNoDice:
    #   pass  # lets just write the damn empty notebook then
    return self._write_empty_notebook(output_filepath)

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
        return self._handle_git_show_128_error(
          input_filepath,
          filename,
          output_filepath,
          output_dir,
          commit)
      else:
        raise e
    else:
      write_file(output_dir, filename, content)
      return output_filepath

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
