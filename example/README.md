nbcrack.py Tutorial
======================

This is a far-too-simple example of using the tool to
convert from ipynb files to python and plain text files.

_TODO_: Create an example with a non-trivial diff that wouldn't normally work in git diff.

This assumes you've already taken the steps to build and install `nbcrack`

Generating code
---------------

Lets start by changing the working directory to the root directory of the repo, e.g.:
```
$ cd nbcrack/
```

Run as follows:
```
$ nbcrack --output_dir example/nbcrack_generated ./example/def_wikipedia_visualization.ipynb
...
finished: generated content for 1 ipynb file(s) in example/nbcrack_generated/
```

See the generated code:
```
example/
├── def_wikipedia_visualization.ipynb
└── nbcrack_generated
    ├── data.json
    ├── def_wikipedia_visualization.ipynb.py
    ├── def_wikipedia_visualization.ipynb.rst
    └── readme.txt
```

Lets commit that code:
```
git add example/nbcrack_generated/
git commit -m "committing auto-generated ipynb files"
```

Displaying generated changes
----------------------------

Try changing the ipynb source file:
```
filename=example/def_wikipedia_visualization.ipynb
perl -pi -e 's/from wand.image import Image as WImage/from wand.image import Image as OOPS/g' $filename
perl -pi -e 's/english 1.20478510204 12.656038024/english nan nan/g' $filename
```

Rerun the tool:
```
$ nbcrack --output_dir example/nbcrack_generated ./example/def_wikipedia_visualization.ipynb
...
finished: generated content for 1 ipynb file(s) in example/nbcrack_generated/
```

See our diff:
```
$ git status
On branch master
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git checkout -- <file>..." to discard changes in working directory)

    modified:   example/def_wikipedia_visualization.ipynb
    modified:   example/nbcrack_generated/data.json
    modified:   example/nbcrack_generated/def_wikipedia_visualization.ipynb.py
    modified:   example/nbcrack_generated/def_wikipedia_visualization.ipynb.rst

no changes added to commit (use "git add" and/or "git commit -a")

$ git diff
... < shows diff >
```

Reverting changes
-----------------

We can show that removing the changes removes the differences:
```
$ git checkout -- def_wikipedia_visualization.ipynb
$ nbcrack --output_dir example/nbcrack_generated ./example/def_wikipedia_visualization.ipynb
...
$ git status
On branch master
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git checkout -- <file>..." to discard changes in working directory)

    modified:   example/nbcrack_generated/data.json
```

The only remaining modified file is a data file that shows the timestamp
of the last conversion from ipynb files to python and plain text files.

Voila! We proved the tool helps us see a human-readable diff of our jupyter notebook.
