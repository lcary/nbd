
from abc import (ABCMeta, abstractmethod)
from os import path as ospath
import logging

import nbformat
from nbconvert import (PythonExporter, RSTExporter)

from .fileops import (get_file_id, write_file)

EXPORT_FORMAT_PYTHON = 'python'
EXPORT_FORMAT_RST = 'rst'

logger = logging.getLogger()


class ExporterWrapper(object):
  FILE_EXTENSION = NotImplemented

  __metaclass__ = ABCMeta

  @abstractmethod
  def export(self, basename, notebook_node, filepath):
    raise NotImplementedError('Exporter wrapper not implemented.')

  def _export_content(self, notebook_node, filepath):
    """
    Exports notebook data in a given format to a file in the output dir.
    Returns notebook content and resources.
    """
    (content, resources) = self.exporter.from_notebook_node(notebook_node)
    write_file(filepath, content, write_mode='w')
    return (content, resources)

  @classmethod
  def _get_filepath(cls, output_dir, basename):
    filename = "{}.{}".format(basename, cls.FILE_EXTENSION)
    return ospath.join(output_dir, filename)


class PythonExporterWrapper(ExporterWrapper):
  FILE_EXTENSION = '.py'

  def __init__(self):
    self.exporter = PythonExporter()

  def export(self, basename, notebook_node, output_dir):
    """
    Exports notebook data in python format.
    """
    filepath = self._get_filepath(output_dir, basename)
    self._export_content(notebook_node, filepath)


class RSTExporterWrapper(ExporterWrapper):
  FILE_EXTENSION = '.rst'

  def __init__(self):
    self.exporter = RSTExporter()

  def export(self, basename, notebook_node, output_dir):
    """
    Exports notebook data in rst format.
    """
    filepath = self._get_filepath(output_dir, basename)
    (content, resources) = self._export_content(notebook_node, filepath)
    self._export_resources(basename, output_dir, resources)

  def _export_resources(self, basename, output_dir, resources):
    """
    Exports any additional resources (e.g. PNG files in notebook)
    """
    try:
      for (filename, b64data) in resources['outputs'].items():
        filename = get_file_id(basename + "__" + filename)
        filepath = ospath.join(output_dir, filename)
        write_file(filepath, b64data, write_mode='wb')
    except AttributeError:
      logger.debug('Unable to find resources in notebook when exporting RST.')


class NotebookExporter(object):
  """
  Process a list of notebooks by creating a directory and exporting
  notebooks to the specified formats (python, rst, and binary files)
  """
  DEFAULT_EXPORT_FORMATS = (EXPORT_FORMAT_PYTHON, EXPORT_FORMAT_RST)

  def __init__(self, output_dir, export_formats=None):
    self.output_dir = output_dir
    self._export_formats = self._get_export_formats(export_formats)
    self.python_exporter = PythonExporterWrapper()
    self.rst_exporter = RSTExporterWrapper()

  def _get_export_formats(self, export_formats):
    if export_formats is None:
      return list(self.DEFAULT_EXPORT_FORMATS)
    else:
      return export_formats

  def process_notebook(self, basename, filepath, nbformat_version):
    """
    Reads a notebook of a given format, then exports data.
    """
    notebook_node = nbformat.read(filepath, as_version=nbformat_version)
    if EXPORT_FORMAT_PYTHON in self._export_formats:
      self.python_exporter.export(basename, notebook_node, self.output_dir)
    if EXPORT_FORMAT_RST in self._export_formats:
      self.rst_exporter.export(basename, notebook_node, self.output_dir)

  def process_notebooks(self, notebook_filepaths, nbformat_version):
    """
    Loads and exports notebooks to a predetermined set of formats.
    """
    for fp in notebook_filepaths:
      basename = get_file_id(fp)
      self.process_notebook(basename, fp, nbformat_version)
