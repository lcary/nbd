nbd
===

A lightweight ipython/jupyter notebook diffing tool.

Purpose
-------

This tool makes ipython/jupyter notebook diffs more readable.

This tool is meant for text-based diffing from the command-line.

Overview
--------

Running `ndb` shows differences in the following types of data:

* Python code
* reStructuredText code
* Resource files (e.g. PNGs)

This will show you most of what has changed in the `In[1]:` and
`Out[1]:` lines of the notebook.

The output of `ndb` is [git-diff] output and can be piped to other
commands like [less(1)] and [tee(1)].

Requirements
------------

* Python >= 2.6
* nbconvert
* pandoc
* git

Install
-------

Install with pip (or your favorite python package manager):
```
pip install nbd
```

Usage
-----

Help:
```
nbd -h
```

Simple usage:
```
nbd <notebook>
```

Pipe to [less(1)]:
```
nbd <notebook> | less
```

Options (see help for all):
```
nbd -e python <notebook>
nbd <notebook1> <notebook2> <notebook3>
nbd <notebook> --git-diff-option="--name-only"
```

Build and install from sources
------------------------------

Source distribution:
```
python setup.py sdist
```

After building, install with pip:
```
pip install dist/nbd-$version.tar.gz
```

Install in a virtual environment to avoid system pip issues.

Tutorial
--------

See the tutorial in the `demo/` directory: [demo tutorial](demo/TUTORIAL.md).

<!-- links: -->

[git-diff]: https://git-scm.com/docs/git-diff
[less(1)]: https://linux.die.net/man/1/less
[tee(1)]: https://linux.die.net/man/1/tee
