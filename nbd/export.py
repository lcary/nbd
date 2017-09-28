import nbformat
from nbconvert import (PythonExporter, RSTExporter)

from .fileops import (get_file_id, write_file)


class NotebookExporter(object):
  """
  Process a list of notebooks by creating a directory and exporting
  notebooks to the specified formats (python, rst, and binary files)
  """
  RUNTIME_DATA_FILENAME = 'data.json'

  def __init__(self, output_dir):
    self.output_dir = output_dir
    self.python_exporter = PythonExporter()
    self.rst_exporter = RSTExporter()

  def process_notebook(self, basename, filepath, nbformat_version):
    """
    Reads a notebook of a given format, then exports data.
    """
    notebook_node = nbformat.read(filepath, as_version=nbformat_version)
    self.export_python(basename, notebook_node)
    self.export_rst_files(basename, notebook_node)

  def process_notebooks(self, notebook_filepaths, nbformat_version):
    """
    Loads and exports notebooks to a predetermined set of formats.
    """
    for fp in notebook_filepaths:
      basename = get_file_id(fp)
      self.process_notebook(basename, fp, nbformat_version)

  def export_python(self, basename, notebook_node):
    """
    Exports notebook data in python format.
    """
    (content, resources) = self.python_exporter.from_notebook_node(notebook_node)

    # write python file
    py_filename = basename + '.py'
    write_file(self.output_dir, py_filename, content, write_mode='w')

  def export_rst_files(self, basename, notebook_node):
    """
    Exports notebook data in rst format.
    """
    (content, resources) = self.rst_exporter.from_notebook_node(notebook_node)

    # write rst file
    rst_filename = basename + '.rst'
    write_file(self.output_dir, rst_filename, content, write_mode='w')

    # write any additional resources (e.g. PNGs)
    for (res_filename, b64data) in resources['outputs'].items():
      res_filepath = get_file_id(basename + "__" + res_filename)
      write_file(self.output_dir, res_filepath, b64data, write_mode='wb')
