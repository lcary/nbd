import os
import sys

PKG_DIR = '../{}'.format('nbd')
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), PKG_DIR)))

import git
