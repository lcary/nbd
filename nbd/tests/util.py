from contextlib import contextmanager
import sys

from mock import patch

def builtins_module():
  """
  Python3 renames the __builtin__ module to builtins.
  This function returns whichever is correct for the python version.
  """
  if sys.version_info >= (3, 0):
    return "builtins.open"
  else:
    return "__builtin__.open"

@contextmanager
def mock_write_file(mock_open_object):
  """
  This function mocks parts of the write_file() function from fileops.py
  which would otherwise interfere with tests.

  Requires a mock.mock_open() argument to be passed in.
  """
  try:
    with patch(builtins_module(), mock_open_object):
      # patch the fileops.py filesystem function calls
      with patch('nbd.fileops.ospath.getsize'):
        yield
  finally:
    pass
