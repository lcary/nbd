
nbd tutorial
============

This tutorial assumes you've already taken the steps to build and install :code:`nbd`.

The tutorial explains:
1. how :code:`nbd` exports notebooks to different formats on demand
2. how the user can diff a notebook easily and relatively quickly

Check for changes
-----------------

Lets start by changing the working directory to the :code:`demo/`
directory in the repo, e.g.:

.. code-block::

    [demo@nbd]$ cd ~/workspace/nbd/demo

Run as follows:

.. code-block::

    [demo@nbd]$ nbd demo.ipynb

There was no output, so we conclude there was no diff to the file. Git confirms:

.. code-block::

    [demo@nbd]$ git status
    On branch demo
    nothing to commit, working tree clean

Displaying notebook changes
---------------------------

Below, we'll demonstrate that :code:`nbd` can make it easy to see
resource file modifications in addition to RST and Python changes.

First, change the ipynb source file via quick and dirty find-replace:

.. code-block::

    [demo@nbd]$ perl -pi -e 's/2 \* np.pi/2.1 \* np.pi/g' demo.ipynb

Then:

#. open this demo.ipynb notebook up with :code:`jupyter notebook`
#. re-run all code blocks to regenerate outputs
#. re-save the file

Run nbd and pipe to :code:`less(1)` to shows a pretty readable diff:

.. code-block:: diff

    [demo@nbd]$ nbd demo.ipynb | less
    diff --git a/var/folders/c1/83dlqbss5w7gh3ywffq3yb600000gn/T/tmpQdQOoi/old/demo__demo.ipynb.py b/var/folders/c1/83dlqbss5w7gh3ywffq3yb600000gn/T/tmpQdQOoi/new/demo__demo.ipynb.py
    index d93157c..a806a3f 100644
    --- a/var/folders/c1/83dlqbss5w7gh3ywffq3yb600000gn/T/tmpQdQOoi/old/demo__demo.ipynb.py
    +++ b/var/folders/c1/83dlqbss5w7gh3ywffq3yb600000gn/T/tmpQdQOoi/new/demo__demo.ipynb.py
    @@ -1,7 +1,7 @@

     # coding: utf-8

    -# In[1]:
    +# In[2]:


     """
    @@ -22,7 +22,7 @@ import numpy as np


     # Simple data to display in various forms
    -x = np.linspace(0, 2 * np.pi, 400)
    +x = np.linspace(0, 2.1 * np.pi, 400)
     y = np.sin(x ** 2)

     plt.close('all')
    diff --git a/var/folders/c1/83dlqbss5w7gh3ywffq3yb600000gn/T/tmpQdQOoi/old/demo__demo.ipynb.rst b/var/folders/c1/83dlqbss5w7gh3ywffq3yb600000gn/T/tmpQdQOoi/new/demo__demo.ipynb.rst
    index d2eb065..63f65db 100644
    --- a/var/folders/c1/83dlqbss5w7gh3ywffq3yb600000gn/T/tmpQdQOoi/old/demo__demo.ipynb.rst
    +++ b/var/folders/c1/83dlqbss5w7gh3ywffq3yb600000gn/T/tmpQdQOoi/new/demo__demo.ipynb.rst
    @@ -24,7 +24,7 @@
     .. code:: ipython2

         # Simple data to display in various forms
    -    x = np.linspace(0, 2 * np.pi, 400)
    +    x = np.linspace(0, 2.1 * np.pi, 400)
         y = np.sin(x ** 2)

         plt.close('all')
    @@ -59,26804 +59,26804 @@

     .. parsed-literal::

So we see the :code:`np.linspace()` code's args change as expected.

If we continue scrolling, the :code:`nbd` diff is much more readable than
if we try to git-diff the demo.ipynb source code directly with git.
Try it out with :code:`git diff demo.ipynb`. You'll see a ton of lines that
only display changes to the image binary file code inline, and it's essentially
a JSON diff. The notebook's image changed since the arguments passed to
:code:`np.linspace()` end up changing the image generated by the code.

Displaying notebook image changes
---------------------------------

So where's the image code in the :code:`nbd` diff? Scrolling down to the
end of the diff, we see a PNG (:code:`demo__demo.ipynb__output_3_0.png`) has changed:

.. code-block:: diff

    [demo@nbd]$ nbd demo.ipynb | tail -n 5
    +      6.54774048  6.56427518  6.58080987  6.59734457]

    diff --git a/var/folders/c1/83dlqbss5w7gh3ywffq3yb600000gn/T/tmprcSHbr/old/demo__demo.ipynb__output_3_0.png b/var/folders/c1/83dlqbss5w7gh3ywffq3yb600000gn/T/tmprcSHbr/new/demo__demo.ipynb__output_3_0.png
    index 8173155..ec4a56d 100644
    Binary files a/var/folders/c1/83dlqbss5w7gh3ywffq3yb600000gn/T/tmprcSHbr/old/demo__demo.ipynb__output_3_0.png and b/var/folders/c1/83dlqbss5w7gh3ywffq3yb600000gn/T/tmprcSHbr/new/demo__demo.ipynb__output_3_0.png differ

We can also easily pass through an option to the :code:`git-diff` command
in order to exclusively view files that have changed:

.. code-block:: diff

    [demo@nbd]$ nbd demo.ipynb --git-diff-options="--name-only"
    2017-09-28 02:40:21,157 - INFO - nbd: git diff output below (no output == no diff)
    /var/folders/c1/83dlqbss5w7gh3ywffq3yb600000gn/T/tmpOkukrd/new/demo__demo.ipynb.py
    /var/folders/c1/83dlqbss5w7gh3ywffq3yb600000gn/T/tmpOkukrd/new/demo__demo.ipynb.rst
    /var/folders/c1/83dlqbss5w7gh3ywffq3yb600000gn/T/tmpOkukrd/new/demo__demo.ipynb__output_3_0.png

This shows there are Python, RST, and PNG file changes to our notebook.
