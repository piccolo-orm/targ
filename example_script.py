import typing as t

from targ import CLI


def echo(message: str):
    """
    Echo back the message.

    :param message:
        What will be printed out.

    """
    print(message)


def add(a: int, b: int):
    """
    Add the two numbers.

    :param a:
        The first number.
    :param b:
        The second number.
    """
    print(a + b)


def say_hello(name: str, greeting: t.Optional[str] = "hello"):
    """
    Greet someone.

    Example usage on the command line:

    say_hello daniel --greeting='bonjour'
    >>> bonjour daniel

    :param name:
        The person to greet.
    :param greeting:
        What to say to the person.

    """
    print(f"{greeting} {name}")


if __name__ == "__main__":
    cli = CLI()
    cli.register(say_hello)
    cli.register(echo)
    cli.register(add)
    cli.run()
