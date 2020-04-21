Supported Types
===============

Targ currently supports basic Python types:

 * str
 * int
 * bool
 * float

You must specify a type annotation for all function arguments, so Targ can
convert the input it receives from the command line into the correct type.

str
---

.. code-block:: python

    def say_hello(name: str):
        print(f'hello {name}')

Example usage:

.. code-block:: bash

    >>> python main.py say_hello bob
    'bob'

    >>> python main.py say_hello --name=bob
    'bob'

When your string contains spaces, use quotation marks:

.. code-block:: bash

    >>> python main.py say_hello --name="bob jones"
    'bob jones'

int
---

.. code-block:: python

    def add(a: int, b: int):
        print(a + b)

Example usage:

.. code-block:: bash

    >>> python main.py add 1 2
    3

    >>> python main.py add --a=1 --b=2
    3

bool
----

.. code-block:: python

    def print_pi(precise: bool = False):
        if precise:
            print("3.14159265")
        else:
            print("3.14")

Example usage:

.. code-block:: bash

    >>> python main.py print_pi
    3.14

    >>> python main.py print_pi true
    3.14159265

    >>> python main.py print_pi --precise
    3.14159265

    >>> python main.py print_pi --precise=true
    3.14159265

You can use `t` as an alias for `true`, and likewise `f` as an alias for
`false`.

.. code-block:: bash

    >>> python main.py print_pi --precise=t
    3.14159265

float
-----

.. code-block:: python

    def compound_interest(interest_rate: float, years: int):
        print(((interest_rate + 1) ** years) - 1)

Example usage:

.. code-block:: bash

    >>> python main.py compound_interest 0.05 5
    0.27628156250000035
