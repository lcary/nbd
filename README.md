ipynb_diff
==========

Generates code for each ipynb input script for human-readable diff viewing.

Purpose
-------

The intent of this project is for text-based diff-viewing. For something
more advanced, see: https://nbdime.readthedocs.io/en/latest/

Requirements
------------

* Python >= 2.6
* virtualenv (optional)
* pandoc

Using virtualenv is optional but recommended to avoid system issues.

Setting up a virtualenv:
* I prefer: https://virtualenvwrapper.readthedocs.io/en/latest/
* Many people use: https://virtualenv.pypa.io/en/stable/

Installing the python requirements:
```
pip install -r requirements.txt
```

The requirements.txt file was originally generated by running:
```
pip install jupyter
pip freeze > requirements.txt
```

The pandoc universal document converter can be installed with:
```
brew install pandoc
```
