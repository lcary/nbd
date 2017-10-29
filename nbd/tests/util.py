from contextlib import contextmanager

from mock import patch


@contextmanager
def mock_write_file(mock_open_object):
  # mock parts of the write_file function from fileops.py that
  # would otherwise interfere with tests. keep tabs on open() calls.
  try:
    with patch("__builtin__.open", mock_open_object):
      with patch('nbd.fileops.ospath.getsize'):
        yield
  finally:
    pass
