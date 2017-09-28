nbd tutorial
============

This is a far-too-simple example of using the tool to
convert from ipynb files to python and plain text files.

_TODO_: Create an example with a non-trivial diff that wouldn't normally work in git diff.

This assumes you've already taken the steps to build and install `nbd`

Check for changes
-----------------

Lets start by changing the working directory to the root directory of the repo, e.g.:
```
[demo@nbd]$ cd ~/workspace/nbd/
```

Run as follows:
```
[demo@nbd]$ ./test_run.sh example/def_wikipedia_visualization.ipynb
2017-09-28 01:31:20,866 - INFO - nbd: git diff output below (no output == no diff)
[demo@nbd]$
```

There was no output, so we conclude there was no diff to the file. Git confirms:
```
[demo@nbd]$ git status
On branch demo
nothing to commit, working tree clean
```

Displaying notebook changes
---------------------------

Try changing the ipynb source file:
```
[demo@nbd]$ filename=example/def_wikipedia_visualization.ipynb
[demo@nbd]$ perl -pi -e 's/from wand.image import Image as WImage/from wand.image import Image as OOPS/g' $filename
[demo@nbd]$ perl -pi -e 's/english 1.20478510204 12.656038024/english nan nan/g' $filename
```

See our diff:
```
[demo@nbd]$ git status
On branch demo
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git checkout -- <file>..." to discard changes in working directory)

  modified:   example/def_wikipedia_visualization.ipynb

no changes added to commit (use "git add" and/or "git commit -a")
```

Rerun the tool:
```diff
[demo@nbd]$ ./test_run.sh ./example/def_wikipedia_visualization.ipynb
2017-09-28 01:33:58,655 - INFO - nbd: git diff output below (no output == no diff)
diff --git a/var/folders/c1/83dlqbss5w7gh3ywffq3yb600000gn/T/tmpkGMobh/old/example__def_wikipedia_visualization.ipynb.py b/var/folders/c1/83dlqbss5w7gh3ywffq3yb600000gn/T/tmpkGMobh/new/example__def_wikipedia_visualization.ipynb.py
index 0a13b7c..96f50a8 100644
--- a/var/folders/c1/83dlqbss5w7gh3ywffq3yb600000gn/T/tmpkGMobh/old/example__def_wikipedia_visualization.ipynb.py
+++ b/var/folders/c1/83dlqbss5w7gh3ywffq3yb600000gn/T/tmpkGMobh/new/example__def_wikipedia_visualization.ipynb.py
@@ -21,7 +21,7 @@ import sys
 sys.path += ['../scripts/']
 from utils import *
 from pyx import *
-from wand.image import Image as WImage
+from wand.image import Image as OOPS
 from def_visualization import *


diff --git a/var/folders/c1/83dlqbss5w7gh3ywffq3yb600000gn/T/tmpkGMobh/old/example__def_wikipedia_visualization.ipynb.rst b/var/folders/c1/83dlqbss5w7gh3ywffq3yb600000gn/T/tmpkGMobh/new/example__def_wikipedia_visualization.ipynb.rst
index ba2e09d..98303ea 100644
--- a/var/folders/c1/83dlqbss5w7gh3ywffq3yb600000gn/T/tmpkGMobh/old/example__def_wikipedia_visualization.ipynb.rst
+++ b/var/folders/c1/83dlqbss5w7gh3ywffq3yb600000gn/T/tmpkGMobh/new/example__def_wikipedia_visualization.ipynb.rst
@@ -31,7 +31,7 @@ Topic visualizations of a Poisson-Gamma DEF (size 50-25-10) trained on 1,000 wik
     sys.path += ['../scripts/']
     from utils import *
     from pyx import *
-    from wand.image import Image as WImage
+    from wand.image import Image as OOPS
     from def_visualization import *

 .. code::
@@ -664,7 +664,7 @@ First layer topics
     england 2.6975768559 17.0423911477
     alfred 1.92078374037 17.0395137256
     ashes 1.2636940781 13.6353682659
-    english 1.20478510204 12.656038024
+    english nan nan
     saxon 1.11993914519 17.3754012034
     australia 1.11208906996 13.9044711631
     series 1.1038239231 10.1592295859
[demo@nbd]$
```

We see a diff to both a Python and RST file here.
This is expected from the find-replace `perl` commands above.

Note that all diffs occur in a temporary directory.
Rerunning those commands will fail, since a directory is created
and destroyed with every run of `nbd` via a `contextmanager`.

Reverting changes
-----------------

We can show that removing the changes removes the differences:
```
[demo@nbd]$ git checkout -- example/def_wikipedia_visualization.ipynb
[demo@nbd]$ ./test_run.sh ./example/def_wikipedia_visualization.ipynb
2017-09-28 01:34:40,962 - INFO - nbd: git diff output below (no output == no diff)
[demo@nbd]$
```

Again, no output.

Voila! We proved the tool helps us see a human-readable diff of our jupyter notebook.
