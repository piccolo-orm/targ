from unittest import TestCase

from targ import CLI


class CLITest(TestCase):
    def test_register(self):
        cli = CLI()

        def hello(name: str):
            print(name)

        cli.register(hello)
