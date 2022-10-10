CLI
===

Registering functions
---------------------

Once you've defined your functions, you need to register them with a ``CLI``
instance.

You can register as many functions as you like with the ``CLI`` instance.

.. code-block:: python

    from targ import CLI


    def add(a: int, b: int):
        print(a + b)


    def subtract(a: int, b: int):
        print(a - b)


    if __name__ == "__main__":
        cli = CLI()
        cli.register(add)
        cli.register(subtract)
        cli.run()

-------------------------------------------------------------------------------

Coroutines
----------

You can also register coroutines, as well as normal functions:

.. code-block:: python

    import asyncio

    from targ import CLI


    async def timer(seconds: int):
        print(f"Sleeping for {seconds}")
        await asyncio.sleep(seconds)
        print("Finished")


   if __name__ == "__main__":
      cli = CLI()
      cli.register(timer)
      cli.run()

-------------------------------------------------------------------------------

Aliases
-------

You can specify aliases for each command, which can make your CLI more
convenient to use. For example, an alias could be an abbreviation, or a common
mispelling.

.. code-block:: python

    from targ import CLI


    def add(a: int, b: int):
        print(a + b)


    if __name__ == "__main__":
        cli = CLI()
        cli.register(add, aliases=['+', 'sum'])
        cli.run()

All of the following will now work:

.. code-block:: bash

    python main.py add 1 1
    python main.py + 1 1
    python main.py sum 1 1

-------------------------------------------------------------------------------

Groups
------

You can add your functions / coroutines to a group:

.. code-block:: python

    cli.register(say_hello, 'greetings')
    cli.register(add, 'maths')

And then call them as follows:

.. code-block:: bash

    python main.py greetings say_hello 'bob'
    python main.py maths add 1 2

-------------------------------------------------------------------------------

Overriding the command name
---------------------------

By default the command name is the name of the function being registered.
However, you can choose to override it:

.. code-block:: python

    cli.register(add, command_name='sum')

-------------------------------------------------------------------------------

Traceback
---------

By default, ``targ`` will print out an abbreviated error message if it encounters
a problem. To see the full Python traceback, pass in the ``--trace`` argument.

.. code-block:: bash

    python main.py maths add 1 'abc' --trace

-------------------------------------------------------------------------------

Solo mode
---------

Sometimes you'll just want to register a single command with your CLI, in which
case, specifying the command name is redundant.

.. code-block:: python

    from targ import CLI


    def add(a: int, b: int):
        print(a + b)


    if __name__ == "__main__":
        cli = CLI()
        cli.register(add)
        cli.run(solo=True)

You can then omit the command name:

.. code-block:: bash

    python main.py 1 1

-------------------------------------------------------------------------------

Source
------

.. currentmodule:: targ

.. autoclass:: CLI
    :members:
