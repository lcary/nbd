from .context import export
from .util import mock_write_file

from mock import (mock_open, patch)
import pytest

TEST_EXTENSION = 'Test'
TEST_NB_BASENAME = 'test_notebook'
TEST_NB_CONTENT = 'This is my test notebook.'
TEST_NB_OUTPUT_DIR = '/output'
TEST_NB_FORMAT_VERSION = 4
TEST_NB_RESOURCE_NAME_1 = 'resource1'
TEST_NB_RESOURCE_NAME_2 = 'resource2'
TEST_NB_RESOURCE_DATA_1 = 00000000000000000000000000000001
TEST_NB_RESOURCE_DATA_2 = 10000000000000000000000000000000


# ----------------------------- Test Classes -----------------------------


class ExporterStub(object):

  def from_notebook_node(self, node):
    content, resources = (TEST_NB_CONTENT, None)
    return (content, resources)


class ExporterWrapperStub(export.ExporterWrapper):
  FILE_EXTENSION = TEST_EXTENSION

  def __init__(self):
    self.exporter = ExporterStub()

  def export(self):
    pass


# ----------------------------- Test Fixtures ----------------------------


@pytest.fixture
def exporter_wrapper():
  return ExporterWrapperStub()


@pytest.fixture
def python_exporter_wrapper():
  return export.PythonExporterWrapper()


@pytest.fixture
def rst_exporter_wrapper():
  return export.RSTExporterWrapper()


@pytest.fixture
def empty_resources():
  return {'outputs': {}}


@pytest.fixture
def some_resources():
  return {'outputs': {
    TEST_NB_RESOURCE_NAME_1: TEST_NB_RESOURCE_DATA_1,
    TEST_NB_RESOURCE_NAME_2: TEST_NB_RESOURCE_DATA_2
  }}


@pytest.fixture
def notebook_exporter():
  return export.NotebookExporter(TEST_NB_FORMAT_VERSION)


# ------------------------------ Test Cases ------------------------------


def test_export_wrapper():
  # can't initialize base class
  with pytest.raises(TypeError):
    export.ExporterWrapper()


def test_export_wrapper_subclass(exporter_wrapper):
  assert exporter_wrapper.FILE_EXTENSION == TEST_EXTENSION


def test_export_content(exporter_wrapper):
  m = mock_open()
  with patch("__builtin__.open", m):
    with patch('nbd.fileops.ospath'):
      exporter_wrapper._export_content("TestNotebook", TEST_NB_BASENAME)
  handle = m()
  handle.write.assert_called_once_with(TEST_NB_CONTENT)


def test_get_filepath(exporter_wrapper):
  expect = 'mydir/myfile.{}'.format(TEST_EXTENSION)
  assert exporter_wrapper._get_filepath('mydir', 'myfile') == expect


def test_python_exporter(python_exporter_wrapper, empty_resources):
  m = mock_open()

  with mock_write_file(m):
    with patch('nbd.export.PythonExporter.from_notebook_node') as mock_func:
      mock_func.return_value = (TEST_NB_CONTENT, empty_resources)
      python_exporter_wrapper.export(TEST_NB_BASENAME, "TestNotebook", TEST_NB_OUTPUT_DIR)

  m.assert_called_once_with('{}/test_notebook.py'.format(TEST_NB_OUTPUT_DIR), 'w')
  handle = m()
  handle.write.assert_called_once_with(TEST_NB_CONTENT)


def test_rst_exporter_no_resources(rst_exporter_wrapper, empty_resources):
  m = mock_open()

  with mock_write_file(m):
    with patch('nbd.export.RSTExporter.from_notebook_node') as mock_func:
      mock_func.return_value = (TEST_NB_CONTENT, empty_resources)
      rst_exporter_wrapper.export(TEST_NB_BASENAME, "TestNotebook", TEST_NB_OUTPUT_DIR)

  m.assert_called_once_with('{}/test_notebook.rst'.format(TEST_NB_OUTPUT_DIR), 'w')
  handle = m()
  handle.write.assert_called_once_with(TEST_NB_CONTENT)


def test_rst_exporter_with_resources(rst_exporter_wrapper, some_resources):
  m = mock_open()
  basename = TEST_NB_BASENAME
  output_dir = TEST_NB_OUTPUT_DIR

  with mock_write_file(m):
    with patch('nbd.export.RSTExporter.from_notebook_node') as mock_func:
      mock_func.return_value = (TEST_NB_CONTENT, some_resources)
      rst_exporter_wrapper.export(basename, "TestNotebook", output_dir)

  get_fp = rst_exporter_wrapper._get_resource_filepath
  m.assert_any_call('{}/test_notebook.rst'.format(TEST_NB_OUTPUT_DIR), 'w')
  m.assert_any_call(get_fp(output_dir, basename, TEST_NB_RESOURCE_NAME_1), 'wb')
  m.assert_any_call(get_fp(output_dir, basename, TEST_NB_RESOURCE_NAME_2), 'wb')

  handle = m()
  handle.write.assert_any_call(TEST_NB_CONTENT)
  handle.write.assert_any_call(TEST_NB_RESOURCE_DATA_1)
  handle.write.assert_any_call(TEST_NB_RESOURCE_DATA_2)


def test_notebook_exporter(notebook_exporter, empty_resources):
  m = mock_open()
  test_nb_filepath = 'fake/filepath/to/notebook'
  test_nb_node = 'fake-notebook-node'

  with mock_write_file(m):
    with patch('nbd.export.nbformat.read') as nbformat_read:
      nbformat_read.return_value = test_nb_node
      with patch('nbd.export.PythonExporter.from_notebook_node') as mock_py_export:
        mock_py_export.return_value = (TEST_NB_CONTENT, empty_resources)
        with patch('nbd.export.RSTExporter.from_notebook_node') as mock_rst_export:
          mock_rst_export.return_value = (TEST_NB_CONTENT, empty_resources)
          notebook_exporter.process_notebook(
            TEST_NB_BASENAME,
            test_nb_filepath,
            TEST_NB_OUTPUT_DIR)
          nbformat_read.assert_called_once_with(
            test_nb_filepath,
            as_version=TEST_NB_FORMAT_VERSION)
          mock_py_export.assert_called_once_with(test_nb_node)
          mock_rst_export.assert_called_once_with(test_nb_node)
