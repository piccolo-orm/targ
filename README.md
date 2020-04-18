# targ

Build a Python CLI for your app, just using type hints and docstrings.

Just register your type annotated functions, and that's it - there's no special
syntax to learn, and it's super easy.

```python
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

```

And from the command line:

```bash
>>> python main.py add 1 1
2
```
