nbd
===

The lightweight ipython notebook diffing tool

Purpose
-------

To turn ipython/jupyter notebooks into something that can be diffed
by a human. No diff/merge GUI, nothing fancy here. This tool merely
exports data from the notebook into a temporary directory in order
to run a `--no-index` git diff, which can be read by the user, or
piped to `less(1)`, or written to a file.

Exported Data
-------------

* Python Format
* RST Format

Requirements
------------

* Python >= 2.6
* nbconvert
* pandoc
* git

Build
-----

Source distribution:
```
python setup.py sdist
```

Install
-------

Build first, then install with pip:
```
pip install dist/nbd-1.0.0.dev1.tar.gz
```

_NOTE_: If you have not already pip-installed `nbconvert`,
running the above command will install it for you.

Usage
-----

Run from root with:
```
nbd
```

Help:
```
nbd -h
```

Example usage:
```
nbd modified_notebook.ipynb
```

Works OK with `less(1)` for big honkin' diffs:
```
nbd massively_modified_notebook.ipynb | less
```

See more in the `example/` directory.
