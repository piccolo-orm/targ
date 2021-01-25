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
    cli.run(solo=True)
