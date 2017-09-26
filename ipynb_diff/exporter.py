import nbformat
from nbconvert import (PythonExporter, RSTExporter)

from .fileops import (get_file_id, normrelpath, write_file)

class NbConvertExporter(object):

  def __init__(self, output_dir, nbformat_version):
    self.output_dir = output_dir
    self.nbformat_version = nbformat_version
    self.basename = None
    self.notebook = None

  def load(self, filepath, root_dir):
    # relativize filepath
    filepath = normrelpath(filepath, root_dir)

    self.basename = get_file_id(filepath)
    self.notebook = nbformat.read(filepath, as_version=self.nbformat_version)

  def export_python(self):
    python_exporter = PythonExporter()

    # convert the notebook to python format
    (content, resources) = python_exporter.from_notebook_node(self.notebook)

    # write python file
    py_filename = self.basename + '.py'
    write_file(self.output_dir, py_filename, content, write_mode='w')

  def export_rst(self):
    rst_exporter = RSTExporter()

    # convert the notebook to rst format
    (content, resources) = rst_exporter.from_notebook_node(self.notebook)

    # write rst file
    rst_filename = self.basename + '.rst'
    write_file(self.output_dir, rst_filename, content, write_mode='w')

    # write resources
    for (resource_filename, b64data) in resources['outputs']:
      resource_filepath = get_file_id(self.basename + "__" + resource_filename)
      write_file(self.output_dir, resource_filepath, b64data, write_mode='wb')
