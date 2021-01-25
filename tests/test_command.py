from unittest import TestCase
from unittest.mock import MagicMock, patch
import sys
import typing as t

from targ import CLI


def add(a: int, b: int):
    print(a + b)


def greeting(afternoon: bool = False):
    if afternoon:
        print("Good afternoon")
    else:
        print("Good morning")


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
        Make sure invalid group names are rejected.
        """
        with self.assertRaises(ValueError):
            CLI().register(add, group_name="contains spaces")

        # Shouldn't raise an exception
        CLI().register(add, group_name="my_group")

    def test_invalid_command_name(self):
        """
        Make sure invalid app names are rejected.
        """
        with self.assertRaises(ValueError):
            CLI().register(add, command_name="contains spaces")

        # Shouldn't raise an exception
        CLI().register(add, command_name="my_command")

    @patch("targ.CLI.get_cleaned_args")
    def test_no_command(self, get_cleaned_args):
        """
        If no command name is given, then help text should be shown.
        """
        get_cleaned_args.return_value = []
        cli = CLI()
        cli.register(add)

        with patch("targ.CLI.get_help_text") as get_help_text:
            cli.run()
            get_help_text.assert_called_once()

        # And just run it once without patching, to make sure no errors
        # are raised
        cli.run()

    @patch("targ.CLI.get_cleaned_args")
    def test_help_flag(self, get_cleaned_args):
        """
        If the --help flag is passed in, then help text should be shown.
        """
        get_cleaned_args.return_value = ["add", "--help"]
        cli = CLI()
        cli.register(add)

        with patch("targ.Command.print_help") as print_help:
            cli.run()
            print_help.assert_called_once()

        # And just run it once without patching, to make sure no errors
        # are raised
        cli.run()

    @patch("targ.CLI.get_cleaned_args")
    def test_bool_flag(self, get_cleaned_args):
        """
        Test the different formats for boolean flags.
        """
        cli = CLI()
        cli.register(greeting)

        with patch("builtins.print", side_effect=print_) as print_mock:
            get_cleaned_args.return_value = ["greeting"]
            cli.run()
            print_mock.assert_called_with("Good morning")

            for flag in (
                "--afternoon=f",
                "--afternoon=false",
                "--afternoon=False",
            ):
                get_cleaned_args.return_value = ["greeting", flag]
                cli.run()
                print_mock.assert_called_with("Good morning")

            for flag in (
                "--afternoon",
                "--afternoon=t",
                "--afternoon=true",
                "--afternoon=True",
            ):
                get_cleaned_args.return_value = ["greeting", flag]
                cli.run()
                print_mock.assert_called_with("Good afternoon")
