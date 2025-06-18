import asyncio
import decimal
from typing import Optional

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


# print_address --number=1 --street="Royal Avenue" --postcode="XYZ 123"
# --city=London
def print_address(
    number: int, street: str, postcode: str, city: Optional[str] = None
):
    """
    Print out the full address.

    :param number:
        House number, e.g. 8
    :street:
        Street name, e.g. "Royal Avenue"
    :postcode:
        e.g. "XYZ 123"
    :city:
        e.g. London

    """
    address = f"{number} {street}"
    if city is not None:
        address += f", {city}"
    address += f", {postcode}"

    print(address)


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


def compound_interest_decimal(interest_rate: decimal.Decimal, years: int):
    """
    Work out the compound interest over the given number of years.

    :param interest_rate:
        The annual interest rate e.g. 0.05
    :param years:
        The number of years over which to compound.
    """
    print(((interest_rate + 1) ** years) - 1)


def create(username: str):
    """
    Create a new user.

    :param username:
        The new user's username.
    """
    print(f"Creating {username}")


async def timer(seconds: int):
    """
    Countdown for a number of seconds.

    :param seconds:
        The number of seconds to countdown.
    """
    print(f"Sleeping for {seconds}")
    await asyncio.sleep(seconds)
    print("Finished")


def raise_error():
    """
    A command which raises an Exception.
    """
    print("Raising an exception")
    raise ValueError("Something went wrong!")


if __name__ == "__main__":
    cli = CLI()
    cli.register(say_hello)
    cli.register(echo)
    cli.register(add, aliases=["+"])
    cli.register(print_pi)
    cli.register(compound_interest)
    cli.register(compound_interest_decimal)
    cli.register(create, group_name="user")
    cli.register(timer)
    cli.register(add, command_name="sum")
    cli.register(print_address)
    cli.register(raise_error)
    cli.run()
