CLI
===

Registering functions
---------------------

Once you've defined your functions, you need to register them with a `CLI`
instance.

You can register as many functions as you like with the `CLI` instance.

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
