from .context import main

import pytest


def test_parser():
  parser = main._parse_args(['file', '-d', '-l', '-v', '500', '-e', 'python'])
  assert parser.debug
  assert parser.log_to_disk
  assert parser.nbformat_version == 500
  assert parser.export_formats == ['python']
  assert parser.old_commit == 'HEAD'
  assert parser.new_commit is None


def test_parser_failure():
  with pytest.raises(SystemExit):
    main._parse_args(['file', '-e', 'invalidformat'])
