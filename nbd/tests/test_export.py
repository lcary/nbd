from contextlib import contextmanager

from .context import export
from .util import mock_write_file

from mock import (mock_open, patch)
import pytest

TEST_EXTENSION = 'Test'
TEST_BASENAME = 'test_notebook'
TEST_CONTENT = 'This is my test notebook.'
TEST_OUTPUT_DIR = '/output'
TEST_FORMAT_VERSION = 4
TEST_RESOURCE_NAME_1 = 'resource1'
TEST_RESOURCE_NAME_2 = 'resource2'
TEST_RESOURCE_DATA_1 = 1000101001010011
TEST_RESOURCE_DATA_2 = 1111010110101100


# ----------------------------- Test Classes -----------------------------


class ExporterStub(object):

  def from_notebook_node(self, node):
    content, resources = (TEST_CONTENT, None)
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
    TEST_RESOURCE_NAME_1: TEST_RESOURCE_DATA_1,
    TEST_RESOURCE_NAME_2: TEST_RESOURCE_DATA_2
  }}


@pytest.fixture
def notebook_exporter():
  return export.NotebookExporter(TEST_FORMAT_VERSION)


# ------------------------------ Test Cases ------------------------------


def test_export_wrapper_subclass(exporter_wrapper):
  assert exporter_wrapper.FILE_EXTENSION == TEST_EXTENSION


def test_export_content(exporter_wrapper):
  m = mock_open()
  with mock_write_file(m):
    exporter_wrapper._export_content("TestNotebook", TEST_BASENAME)
  handle = m()
  handle.write.assert_called_once_with(TEST_CONTENT)


def test_get_filepath(exporter_wrapper):
  expect = 'mydir/myfile.{}'.format(TEST_EXTENSION)
  assert exporter_wrapper._get_filepath('mydir', 'myfile') == expect


@contextmanager
def mock_nbconvert_and_check_output(mock_target, file_extension):
  m = mock_open()

  try:
    with mock_write_file(m):
      with patch(mock_target) as mock_nbconvert:
        yield mock_nbconvert
  finally:
    output_filepath = '{}/{}.{}'.format(TEST_OUTPUT_DIR, TEST_BASENAME, file_extension)
    m.assert_called_once_with(output_filepath, 'w')
    handle = m()
    handle.write.assert_called_once_with(TEST_CONTENT)


def test_python_exporter(python_exporter_wrapper, empty_resources):
  extension = python_exporter_wrapper.FILE_EXTENSION
  mock_target = 'nbd.export.PythonExporter.from_notebook_node'
  with mock_nbconvert_and_check_output(mock_target, extension) as mock_nbconvert:
    mock_nbconvert.return_value = (TEST_CONTENT, empty_resources)
    python_exporter_wrapper.export(TEST_BASENAME, "TestNotebook", TEST_OUTPUT_DIR)


def test_rst_exporter_no_resources(rst_exporter_wrapper, empty_resources):
  extension = rst_exporter_wrapper.FILE_EXTENSION
  mock_target = 'nbd.export.RSTExporter.from_notebook_node'
  with mock_nbconvert_and_check_output(mock_target, extension) as mock_nbconvert:
    mock_nbconvert.return_value = (TEST_CONTENT, empty_resources)
    rst_exporter_wrapper.export(TEST_BASENAME, "TestNotebook", TEST_OUTPUT_DIR)


def test_rst_exporter_with_resources(rst_exporter_wrapper, some_resources):
  m = mock_open()
  basename = TEST_BASENAME
  output_dir = TEST_OUTPUT_DIR

  with mock_write_file(m):
    with patch('nbd.export.RSTExporter.from_notebook_node') as mock_func:
      mock_func.return_value = (TEST_CONTENT, some_resources)
      rst_exporter_wrapper.export(basename, "TestNotebook", output_dir)

  get_fp = rst_exporter_wrapper._get_resource_filepath
  m.assert_any_call('{}/{}.rst'.format(TEST_OUTPUT_DIR, basename), 'w')
  m.assert_any_call(get_fp(output_dir, basename, TEST_RESOURCE_NAME_1), 'wb')
  m.assert_any_call(get_fp(output_dir, basename, TEST_RESOURCE_NAME_2), 'wb')

  handle = m()
  handle.write.assert_any_call(TEST_CONTENT)
  handle.write.assert_any_call(TEST_RESOURCE_DATA_1)
  handle.write.assert_any_call(TEST_RESOURCE_DATA_2)


def test_notebook_exporter(notebook_exporter, empty_resources):
  m = mock_open()
  test_filepath = 'fake/filepath/to/notebook.ipynb'
  test_node = 'fake-notebook-node'

  with mock_write_file(m):
    with patch('nbd.export.nbformat.read') as nbformat_read:
      nbformat_read.return_value = test_node
      with patch('nbd.export.PythonExporter.from_notebook_node') as mock_py_export:
        mock_py_export.return_value = (TEST_CONTENT, empty_resources)
        with patch('nbd.export.RSTExporter.from_notebook_node') as mock_rst_export:
          mock_rst_export.return_value = (TEST_CONTENT, empty_resources)
          notebook_exporter.process_notebook(
            TEST_BASENAME,
            test_filepath,
            TEST_OUTPUT_DIR)
          nbformat_read.assert_called_once_with(
            test_filepath,
            as_version=TEST_FORMAT_VERSION)
          mock_py_export.assert_called_once_with(test_node)
          mock_rst_export.assert_called_once_with(test_node)
