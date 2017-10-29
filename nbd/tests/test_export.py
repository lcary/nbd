from .context import export

from mock import patch, mock_open
import pytest

TEST_EXTENSION = 'Test'
TEST_NB_CONTENT = 'This is my test notebook.'
TEST_NB_RESOURCES = None

def test_export_wrapper():
    # can't initialize base class
    with pytest.raises(TypeError):
        export.ExporterWrapper()


@pytest.fixture
def exporter_wrapper():

    class TestExporter(object):
        def from_notebook_node(self, node):
            content, resources = (TEST_NB_CONTENT, TEST_NB_RESOURCES)
            return (content, resources)

    class TestExporterWrapper(export.ExporterWrapper):
        FILE_EXTENSION = TEST_EXTENSION
        def __init__(self):
            self.exporter = TestExporter()
        def export(self):
            pass

    return TestExporterWrapper()


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
