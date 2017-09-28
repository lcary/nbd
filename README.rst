nbd
===

The lightweight ipython notebook diffing tool

Purpose
-------

To turn ipython/jupyter notebooks into something that can be diffed by a
human. No diff or merge GUI, nothing fancy here. This tool just exports
data from the notebook to git diff, which can be read by the user, or
piped to ``less(1)``, or written to a file.

Export data
-----------

Running ``ndb`` exports the following data from a notebook:

-  Python Format (the ``In``\ s)
-  RST Format (the ``Out``\ s)
-  Resources (e.g. PNGs)

Requirements
------------

-  Python >= 2.6
-  nbconvert
-  pandoc
-  git

Usage
-----

Help:

::

    nbd -h

Example usage:

::

    nbd modified_notebook.ipynb

Works with ``less(1)`` for big diffs:

::

    nbd massively_modified_notebook.ipynb | less

Build
-----

Source distribution:

::

    python setup.py sdist

Install
-------

Build first, then install with pip:

::

    pip install dist/nbd-1.0.0.dev1.tar.gz

*NOTE*: If you have not already pip-installed ``nbconvert``, running the
above command will install it for you.

Tutorial
--------

See the tutorial in the ``demo/`` directory: `demo
tutorial <demo/TUTORIAL.md>`__.
