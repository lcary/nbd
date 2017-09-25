from os import path as ospath

import logging

logger = logging.getLogger()


def normrelpath(path, root_dir):
  """
  Return a normalized path relative to some root dir.
  """
  return ospath.normpath(ospath.relpath(path, start=root_dir))


def get_file_id(filepath, root_dir):
  """
  Returns a unique identifier based on file path and directory.

  Goals: Use unique keys, e.g. in cases where multiple directories
  contain files with the same names.
  """
  return filepath.replace(ospath.sep, "__")


def write_file(dir_path, filename, content):
  """
  Write content to a file with a given name in a given directory.

  Additionally, log the path where the content was written to.
  """
  abspath = ospath.abspath(ospath.join(dir_path, filename))
  with open(abspath, 'w') as f:
    f.write(content)
  nbytes = ospath.getsize(abspath)
  logger.debug("wrote {} bytes to {}".format(nbytes, abspath))
