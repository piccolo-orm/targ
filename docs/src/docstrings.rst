Docstrings
==========

Docstrings are used to document your CLI.

ReST-style and Google-style docstrings are supported - use whichever you
prefer the look of, as functionally they are basically the same.

-------------------------------------------------------------------------------

ReST
----

.. code-block:: python

    def say_hello(name: str):
        """
        Say hello to someone.

        :param name: The person to say hello to.

        """
        print(f'hello {name}')

-------------------------------------------------------------------------------

Google
------

.. code-block:: python

    def say_hello(name: str):
        """
        Say hello to someone.

        Args:
            name:
                The person to say hello to.

        """
        print(f'hello {name}')

-------------------------------------------------------------------------------

Output
------

Targ automatically documents your API using the docstring:

.. code-block:: bash

    python main.py say_hello --help

.. code-block:: bash

    say_hello
    Say hello to someone.

    Usage:
    say_hello name

    Args:
    name       The person to say hello to.
