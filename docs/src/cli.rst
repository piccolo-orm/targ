CLI
===

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
