Example ipynb_diff.py usage
===========================

This is a far-too-simple example of using the tool.

_TODO_: Create an example with a non-trivial diff that wouldn't normally work in git diff.

Lets start by changing the working directory to this directory, e.g.:
```
$ cd ipynb_diff/example
```

Run as follows:
```
$ ../ipynb_diff_cli ./def_wikipedia_visualization.ipynb
...
finished: generated content for 1 ipynb file(s) in example/ipynb_generated/
```

See the generated code:
```
.
├── def_wikipedia_visualization.ipynb
└── ipynb_generated
    ├── data.json
    ├── def_wikipedia_visualization.ipynb.py
    ├── def_wikipedia_visualization.ipynb.rst
    └── readme.txt
```

Lets commit that code:
```
git add ipynb_generated/
git commit -m "committing auto-generated ipynb files"
```

Try changing the ipynb source file:
```
filename=def_wikipedia_visualization.ipynb
perl -pi -e 's/from wand.image import Image as WImage/from wand.image import Image as OOPS/g' $filename
perl -pi -e 's/english 1.20478510204 12.656038024/english nan nan/g' $filename
```

Rerun the tool:
```
$ ../ipynb_diff_cli ./def_wikipedia_visualization.ipynb
...
finished: generated content for 1 ipynb file(s) in example/ipynb_generated/
```

See our diff:
```
$ git status
On branch master
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git checkout -- <file>..." to discard changes in working directory)

    modified:   def_wikipedia_visualization.ipynb
    modified:   ipynb_generated/data.json
    modified:   ipynb_generated/def_wikipedia_visualization.ipynb.py
    modified:   ipynb_generated/def_wikipedia_visualization.ipynb.rst

no changes added to commit (use "git add" and/or "git commit -a")

$ git diff
... < shows diff >
```

We can show that removing the changes removes the differences:
```
$ git checkout -- def_wikipedia_visualization.ipynb
$ ../ipynb_diff_cli ./def_wikipedia_visualization.ipynb
...
$ git status
On branch master
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git checkout -- <file>..." to discard changes in working directory)

    modified:   ipynb_generated/data.json
```

Voila! We proved the tool helps us see a human-readable diff of our jupyter notebook.
