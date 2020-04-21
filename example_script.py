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


def say_hello(name: str, greeting: str = "hello"):
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


def print_pi(precise: bool = False):
    """
    Print out the digits of Pi.

    :param precise:
        If set, then more digits are printed out.
    """
    if precise:
        print("3.14159265")
    else:
        print("3.14")


def compound_interest(interest_rate: float, years: int):
    """
    Work out the compound interest over the given number of years.

    :param interest_rate:
        The annual interest rate e.g. 0.05
    :param years:
        The number of years over which to compound.
    """
    print(((interest_rate + 1) ** years) - 1)


if __name__ == "__main__":
    cli = CLI()
    cli.register(say_hello)
    cli.register(echo)
    cli.register(add)
    cli.register(print_pi)
    cli.register(compound_interest)
    cli.run()
