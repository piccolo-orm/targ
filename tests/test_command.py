from unittest import TestCase
from unittest.mock import MagicMock, patch
import sys
import typing as t

from targ import CLI


def add(a: int, b: int):
    print(a + b)


def print_(value: t.Any, *args, **kwargs):
    """
    When patching the builtin print statement, this is used as a side effect,
    so we can still use debug statements.
    """
    sys.stdout.write(str(value) + "\n")
    sys.stdout.flush()


class CLITest(TestCase):
    def test_register(self):
        """
        Make sure a command can be registered.
        """
        cli = CLI()

        cli.register(add)

        self.assertTrue(len(cli.commands) == 1)
        self.assertTrue(cli.commands[0].command is add)

    @patch("targ.CLI.get_cleaned_args")
    def test_run(self, get_cleaned_args: MagicMock):
        """
        Make sure a command is run correctly.
        """
        get_cleaned_args.return_value = ["add", "1", "2"]
        cli = CLI()
        cli.register(add)

        with patch("builtins.print", side_effect=print_) as print_mock:
            cli.run()
            print_mock.assert_called_with(3)

    @patch("targ.CLI.get_cleaned_args")
    def test_run_solo(self, get_cleaned_args: MagicMock):
        """
        Make sure a command is run correctly, when the CLI is in solo mode.
        """
        get_cleaned_args.return_value = ["1", "2"]
        cli = CLI()
        cli.register(add)

        with patch("builtins.print", side_effect=print_) as print_mock:
            cli.run(solo=True)
            print_mock.assert_called_with(3)

    @patch("targ.CLI.get_cleaned_args")
    def test_run_group(self, get_cleaned_args: MagicMock):
        """
        Make sure a command is run correctly, when the command has been
        registered in a group.
        """
        get_cleaned_args.return_value = ["math", "add", "1", "2"]
        cli = CLI()
        cli.register(add, group_name="math")

        with patch("builtins.print", side_effect=print_) as print_mock:
            cli.run()
            print_mock.assert_called_with(3)

    def test_invalid_group_name(self):
        """
        Make sure a command is run correctly, when the command has been
        registered in a group.
        """
        with self.assertRaises(ValueError):
            CLI().register(add, group_name="contains spaces")

    def test_invalid_app_name(self):
        """
        Make sure a command is run correctly, when the command has been
        registered in a group.
        """
        with self.assertRaises(ValueError):
            CLI().register(add, command_name="contains spaces")
