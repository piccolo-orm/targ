.. Targ documentation master file, created by
   sphinx-quickstart on Sat Apr 18 23:01:00 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Targ's documentation!
================================

Build a Python CLI for your app, just using type hints and docstrings.

Just register your type annotated functions, and that's it - there's no special
syntax to learn, and it's super easy.

.. code-block:: python

   # main.py
   from targ import CLI


   def add(a: int, b: int):
      """
      Add the two numbers.

      :param a:
         The first number.
      :param b:
         The second number.
      """
      print(a + b)


   if __name__ == "__main__":
      cli = CLI()
      cli.register(add)
      cli.run()


And from the command line:

.. code-block:: bash

   >>> python main.py add 1 1
   2


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation.rst
   supported_types.rst
   docstrings.rst
   cli.rst
   related_projects.rst
