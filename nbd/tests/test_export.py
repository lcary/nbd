from .context import export

from mock import patch, mock_open
import pytest

TEST_EXTENSION = 'Test'
TEST_NB_CONTENT = 'This is my test notebook.'
TEST_NB_RESOURCES = None


class ExporterStub(object):

  def from_notebook_node(self, node):
    content, resources = (TEST_NB_CONTENT, TEST_NB_RESOURCES)
    return (content, resources)


class ExporterWrapperStub(export.ExporterWrapper):
  FILE_EXTENSION = TEST_EXTENSION

  def __init__(self):
    self.exporter = ExporterStub()

  def export(self):
    pass


@pytest.fixture
def exporter_wrapper():
  return ExporterWrapperStub()


@pytest.fixture
def python_exporter_wrapper():
  return export.PythonExporterWrapper()


@pytest.fixture
def rst_exporter_wrapper():
  return export.RSTExporterWrapper()


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
      exporter_wrapper._export_content("TestNotebook", "test_notebook")
  handle = m()
  handle.write.assert_called_once_with(TEST_NB_CONTENT)


def test_get_filepath(exporter_wrapper):
  expect = 'mydir/myfile.{}'.format(TEST_EXTENSION)
  assert exporter_wrapper._get_filepath('mydir', 'myfile') == expect


def test_python_exporter(python_exporter_wrapper):
  m = mock_open()
  with patch("__builtin__.open", m):
    with patch('nbd.fileops.ospath'):
      with patch('nbd.export.PythonExporter.from_notebook_node') as mock_func:
        mock_func.return_value = (TEST_NB_CONTENT, 'resources')
        python_exporter_wrapper.export("test_notebook", "TestNotebook", "output_dir")
  handle = m()
  handle.write.assert_called_once_with(TEST_NB_CONTENT)

