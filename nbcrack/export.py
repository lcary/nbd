from datetime import datetime
import json
import logging

import nbformat
from nbconvert import (PythonExporter, RSTExporter)

from .command import (ANSI_LIGHT_GREEN, echo)
from .const import PKG_NAME
from .fileops import (get_file_id, write_file)

logger = logging.getLogger()


class NotebookExporter(object):
  """
  Processed a list of notebooks by creating a directory and exporting
  notebooks to the specified formats (python, rst, and binary files)

  It expects all paths of notebooks and directories to be relative
  to either the root of a git repo, or some subdirectory therein.
  """

  README_MESSAGE = (
    'The files in {output_dir}/ were automatically generated by '
    '{program}. Do not edit manually.\n')
  RUNTIME_DATA_FILENAME = 'data.json'

  def __init__(self, output_dir):
    self.start_time = datetime.now()
    self.output_dir = output_dir
    self.notebooks_processed = 0
    # delegate exporting to nbexport
    self.python_exporter = PythonExporter()
    self.rst_exporter = RSTExporter()

  def setup(self):
    """
    Bootstraps the output directory with necessary files.
    """
    self._write_readme()
    self._write_gitignore()

  def process(self, filepaths, nbformat_version):
    """
    Loads and exports notebook to a predetermined set of formats.
    """
    for fp in filepaths:
      basename = get_file_id(fp)
      notebook = nbformat.read(fp, as_version=nbformat_version)
      self.export_python(basename, notebook)
      self.export_rst(basename, notebook)
      self.notebooks_processed += 1

  def teardown(self):
    """
    Displays to the user that the program has finished executing,
    and write data about its execution to the output directory.
    """
    self._write_runtime_data(datetime.now())
    msg = "generated content for {} ipynb file(s) in {}/".format(
      self.notebooks_processed, self.output_dir)
    echo("finished", ANSI_LIGHT_GREEN, msg)

  def export_python(self, basename, notebook):
    """
    Exports a pre-loaded notebook in python format.
    """
    (content, resources) = self.python_exporter.from_notebook_node(notebook)

    # write python file
    py_filename = basename + '.py'
    write_file(self.output_dir, py_filename, content, write_mode='w')

  def export_rst(self, basename, notebook):
    """
    Exports a pre-loaded notebook in rst format.
    """
    (content, resources) = self.rst_exporter.from_notebook_node(notebook)

    # write rst file
    rst_filename = basename + '.rst'
    write_file(self.output_dir, rst_filename, content, write_mode='w')

    # write any additional resources
    for (res_filename, b64data) in resources['outputs']:
      res_filepath = get_file_id(self.basename + "__" + res_filename)
      write_file(self.output_dir, res_filepath, b64data, write_mode='wb')

  def _write_readme(self):
    content = self.README_MESSAGE.format(
      output_dir=self.output_dir,
      program=PKG_NAME)
    write_file(self.output_dir, 'readme.txt', content)

  def _write_gitignore(self):
    content = "\n".join(["*.log", self.RUNTIME_DATA_FILENAME])
    write_file(self.output_dir, '.gitignore', content)

  def _write_runtime_data(self, end_time):
    data = dict(
      program=PKG_NAME,
      output_dir=self.output_dir,
      time_started=str(self.start_time),
      time_finished=str(end_time),
      runtime_seconds=(end_time - self.start_time).total_seconds(),
      notebooks_processed=self.notebooks_processed)
    content = json.dumps(data, indent=2, sort_keys=True)
    write_file(self.output_dir, self.RUNTIME_DATA_FILENAME, content)
