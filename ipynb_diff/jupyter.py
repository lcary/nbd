import logging
from subprocess import CalledProcessError

from .command import Command


class JupyterCommand(object):

  def __init__(self, output_dir):
    self.output_dir = output_dir
    self.command = Command()

  class JupyterCommandMissing(Exception):
    pass

  class JupyterCommandFailure(Exception):
    pass

  def _nbconvert(self, filepath, basename, export_fmt):
    args = [
      'jupyter',
      'nbconvert',
      filepath,
      '--output={}'.format(basename),
      '--output-dir={}'.format(self.output_dir),
      '--to={}'.format(export_fmt)]

    try:
      return self.command.run(args)
    except OSError:
      msg = ("The jupyter command was not found on your machine. "
        "Please install all requirements in requirements.txt first.")
      logging.exception("message")
      raise self.JupyterCommandMissing(msg)
    except CalledProcessError:
      logging.exception("message")
      raise self.JupyterCommandFailure("The jupyter command failed.")

  def convert_to_python(self, filepath, basename):
    self._nbconvert(filepath, basename, 'python')

  def convert_to_rst(self, filepath, basename):
    self._nbconvert(filepath, basename, 'rst')
