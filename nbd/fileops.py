from contextlib import contextmanager
from os import path as ospath
import logging
import tempfile
import shutil

logger = logging.getLogger()


def normrelpath(path, root_dir):
  """
  Return a normalized path relative to some root dir.
  """
  return ospath.normpath(ospath.relpath(path, start=root_dir))


def get_file_id(filepath):
  """
  Returns a unique identifier based on file path.

  Goals: Use unique keys, e.g. in cases where multiple directories
  contain files with the same names.
  """
  return filepath.replace(ospath.sep, "__")


def write_file(filepath, content, write_mode='w'):
  """
  Write content to a file with a given name in a given directory.

  Additionally, log the path where the content was written to.
  """
  abspath = ospath.abspath(filepath)
  with open(abspath, write_mode) as f:
    f.write(content)
  nbytes = ospath.getsize(abspath)
  logger.debug("wrote {} bytes to {}".format(nbytes, abspath))


@contextmanager
def mktempdir():
  name = tempfile.mkdtemp()
  try:
    yield name
  finally:
    shutil.rmtree(name)
