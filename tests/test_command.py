import dataclasses
import decimal
import sys
import typing as t
from unittest import TestCase
from unittest.mock import MagicMock, patch

from targ import CLI


def add(a: int, b: int):
    """
    A simple example command.
    """
    print(a + b)


def print_(value: t.Any, *args, **kwargs):
    """
    When patching the builtin print statement, this is used as a side effect,
    so we can still use debug statements.
    """
    sys.stdout.write(str(value) + "\n")
    sys.stdout.flush()


@dataclasses.dataclass
class Config:
    params: t.List[str]
    output: str


class CLITest(TestCase):
    def test_register(self):
        """
        Make sure a command can be registered.
        """
        cli = CLI()

        cli.register(add)

        self.assertTrue(len(cli.commands) == 1)
        self.assertTrue(cli.commands[0].command is add)

    @patch("targ.CLI._get_cleaned_args")
    def test_run(self, _get_cleaned_args: MagicMock):
        """
        Make sure a command is run correctly.
        """
        _get_cleaned_args.return_value = ["add", "1", "2"]
        cli = CLI()
        cli.register(add)

        with patch("builtins.print", side_effect=print_) as print_mock:
            cli.run()
            print_mock.assert_called_with(3)

    @patch("targ.CLI._get_cleaned_args")
    def test_run_solo(self, _get_cleaned_args: MagicMock):
        """
        Make sure a command is run correctly, when the CLI is in solo mode.
        """
        _get_cleaned_args.return_value = ["1", "2"]
        cli = CLI()
        cli.register(add)

        with patch("builtins.print", side_effect=print_) as print_mock:
            cli.run(solo=True)
            print_mock.assert_called_with(3)

    @patch("targ.CLI._get_cleaned_args")
    def test_run_group(self, _get_cleaned_args: MagicMock):
        """
        Make sure a command is run correctly, when the command has been
        registered in a group.
        """
        _get_cleaned_args.return_value = ["math", "add", "1", "2"]
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

    @patch("targ.CLI._get_cleaned_args")
    def test_no_command(self, _get_cleaned_args):
        """
        If no command name is given, then help text should be shown.
        """
        _get_cleaned_args.return_value = []
        cli = CLI()
        cli.register(add)

        with patch("targ.CLI.get_help_text") as get_help_text:
            cli.run()
            get_help_text.assert_called_once()

        # And just run it once without patching, to make sure no errors
        # are raised
        cli.run()

    @patch("targ.CLI._get_cleaned_args")
    def test_help_flag(self, _get_cleaned_args):
        """
        If the --help flag is passed in, then help text should be shown.
        """
        _get_cleaned_args.return_value = ["add", "--help"]
        cli = CLI()
        cli.register(add)

        with patch("targ.Command.print_help") as print_help:
            cli.run()
            print_help.assert_called_once()

        # And just run it once without patching, to make sure no errors
        # are raised
        cli.run()

    @patch("targ.CLI._get_cleaned_args")
    def test_bool_arg(self, _get_cleaned_args: MagicMock):
        """
        Test the different formats for boolean flags.
        """

        def test_command(arg1: bool = False):
            """
            A command for testing boolean arguments.
            """
            if arg1 is True:
                print("arg1 is True")
            elif arg1 is False:
                print("arg1 is False")
            else:
                raise ValueError("arg1 is the wrong type")

        cli = CLI()
        cli.register(test_command)

        with patch("builtins.print", side_effect=print_) as print_mock:

            configs: t.List[Config] = [
                Config(params=["test_command"], output="arg1 is False"),
                Config(params=["test_command", "f"], output="arg1 is False"),
                Config(
                    params=["test_command", "false"], output="arg1 is False"
                ),
                Config(
                    params=["test_command", "False"], output="arg1 is False"
                ),
                Config(
                    params=["test_command", "--arg1=f"], output="arg1 is False"
                ),
                Config(
                    params=["test_command", "--arg1=false"],
                    output="arg1 is False",
                ),
                Config(
                    params=["test_command", "--arg1=False"],
                    output="arg1 is False",
                ),
                Config(params=["test_command", "t"], output="arg1 is True"),
                Config(params=["test_command", "true"], output="arg1 is True"),
                Config(params=["test_command", "True"], output="arg1 is True"),
                Config(
                    params=["test_command", "--arg1"], output="arg1 is True"
                ),
                Config(
                    params=["test_command", "--arg1=t"], output="arg1 is True"
                ),
                Config(
                    params=["test_command", "--arg1=true"],
                    output="arg1 is True",
                ),
                Config(
                    params=["test_command", "--arg1=True"],
                    output="arg1 is True",
                ),
            ]

            for config in configs:
                _get_cleaned_args.return_value = config.params
                cli.run()
                print_mock.assert_called_with(config.output)
                print_mock.reset_mock()

    @patch("targ.CLI._get_cleaned_args")
    def test_optional_bool_arg(self, _get_cleaned_args: MagicMock):
        """
        Test command arguments which are of type Optional[bool].
        """

        def test_command(arg1: t.Optional[bool] = None):
            """
            A command for testing optional boolean arguments.
            """
            if arg1 is None:
                print("arg1 is None")
            elif arg1 is True:
                print("arg1 is True")
            elif arg1 is False:
                print("arg1 is False")
            else:
                raise ValueError("arg1 is the wrong type")

        cli = CLI()
        cli.register(test_command)

        with patch("builtins.print", side_effect=print_) as print_mock:

            configs: t.List[Config] = [
                Config(
                    params=["test_command", "--arg1"],
                    output="arg1 is True",
                ),
                Config(
                    params=["test_command", "--arg1=True"],
                    output="arg1 is True",
                ),
                Config(
                    params=["test_command", "--arg1=true"],
                    output="arg1 is True",
                ),
                Config(
                    params=["test_command", "--arg1=t"],
                    output="arg1 is True",
                ),
                Config(
                    params=["test_command", "--arg1=False"],
                    output="arg1 is False",
                ),
                Config(
                    params=["test_command", "--arg1=false"],
                    output="arg1 is False",
                ),
                Config(
                    params=["test_command", "--arg1=f"],
                    output="arg1 is False",
                ),
                Config(params=["test_command"], output="arg1 is None"),
            ]

            for config in configs:
                _get_cleaned_args.return_value = config.params
                cli.run()
                print_mock.assert_called_with(config.output)
                print_mock.reset_mock()

    @patch("targ.CLI._get_cleaned_args")
    def test_int_arg(self, _get_cleaned_args: MagicMock):
        """
        Test command arguments which are of type int.
        """

        def test_command(arg1: decimal.Decimal):
            """
            A command for testing Decimal arguments.
            """
            if type(arg1) is decimal.Decimal:
                print("arg1 is int")
            else:
                raise ValueError("arg1 is the wrong type")

        cli = CLI()
        cli.register(test_command)

        with patch("builtins.print", side_effect=print_) as print_mock:

            configs: t.List[Config] = [
                Config(
                    params=["test_command", "1"],
                    output="arg1 is int",
                ),
                Config(
                    params=["test_command", "--arg1=1"],
                    output="arg1 is int",
                ),
            ]

            for config in configs:
                _get_cleaned_args.return_value = config.params
                cli.run()
                print_mock.assert_called_with(config.output)
                print_mock.reset_mock()

    @patch("targ.CLI._get_cleaned_args")
    def test_decimal_arg(self, _get_cleaned_args: MagicMock):
        """
        Test command arguments which are of type Decimal.
        """

        def test_command(arg1: decimal.Decimal):
            """
            A command for testing Decimal arguments.
            """
            if type(arg1) is decimal.Decimal:
                print("arg1 is Decimal")
            else:
                raise ValueError("arg1 is the wrong type")

        cli = CLI()
        cli.register(test_command)

        with patch("builtins.print", side_effect=print_) as print_mock:

            configs: t.List[Config] = [
                Config(
                    params=["test_command", "1.11"],
                    output="arg1 is Decimal",
                ),
                Config(
                    params=["test_command", "--arg1=1.11"],
                    output="arg1 is Decimal",
                ),
            ]

            for config in configs:
                _get_cleaned_args.return_value = config.params
                cli.run()
                print_mock.assert_called_with(config.output)
                print_mock.reset_mock()

    @patch("targ.CLI._get_cleaned_args")
    def test_float_arg(self, _get_cleaned_args: MagicMock):
        """
        Test command arguments which are of type float.
        """

        def test_command(arg1: float):
            """
            A command for testing float arguments.
            """
            if type(arg1) is float:
                print("arg1 is float")
            else:
                raise ValueError("arg1 is the wrong type")

        cli = CLI()
        cli.register(test_command)

        with patch("builtins.print", side_effect=print_) as print_mock:

            configs: t.List[Config] = [
                Config(
                    params=["test_command", "1.11"],
                    output="arg1 is float",
                ),
                Config(
                    params=["test_command", "--arg1=1.11"],
                    output="arg1 is float",
                ),
            ]

            for config in configs:
                _get_cleaned_args.return_value = config.params
                cli.run()
                print_mock.assert_called_with(config.output)
                print_mock.reset_mock()

    @patch("targ.CLI._get_cleaned_args")
    def test_mixed_args(self, _get_cleaned_args: MagicMock):
        """
        Test command arguments which are of multiple different types.
        """

        def test_command(arg1: float, arg2: bool):
            """
            A command for testing float arguments.
            """
            if type(arg1) is float and type(arg2) is bool:
                print("arg1 is float, arg2 is bool")
            else:
                raise ValueError("args are the wrong type")

        cli = CLI()
        cli.register(test_command)

        with patch("builtins.print", side_effect=print_) as print_mock:

            configs: t.List[Config] = [
                Config(
                    params=["test_command", "1.11", "true"],
                    output="arg1 is float, arg2 is bool",
                ),
                Config(
                    params=["test_command", "1.11", "--arg2=true"],
                    output="arg1 is float, arg2 is bool",
                ),
                Config(
                    params=["test_command", "--arg1=1.11", "--arg2=true"],
                    output="arg1 is float, arg2 is bool",
                ),
                Config(
                    params=["test_command", "--arg2=true", "--arg1=1.11"],
                    output="arg1 is float, arg2 is bool",
                ),
            ]

            for config in configs:
                _get_cleaned_args.return_value = config.params
                cli.run()
                print_mock.assert_called_with(config.output)
                print_mock.reset_mock()

    @patch("targ.CLI._get_cleaned_args")
    def test_aliases(self, _get_cleaned_args: MagicMock):
        """
        Make sure commands with aliases can be called correctly.
        """

        def test_command():
            print("Command called")

        cli = CLI()
        cli.register(test_command, aliases=["tc"])

        with patch("builtins.print", side_effect=print_) as print_mock:

            configs: t.List[Config] = [
                Config(params=["test_command"], output="Command called"),
                Config(params=["tc"], output="Command called"),
            ]

            for config in configs:
                _get_cleaned_args.return_value = config.params
                cli.run()
                print_mock.assert_called_with(config.output)
                print_mock.reset_mock()

    @patch("targ.CLI._get_cleaned_args")
    def test_no_type_annotations(self, _get_cleaned_args: MagicMock):
        """
        Make sure a command with no type annotations still works - the
        arguments passed to the function will just be strings.
        """

        def test_command(name):
            print(name)

        cli = CLI()
        cli.register(test_command)

        with patch("builtins.print", side_effect=print_) as print_mock:

            configs: t.List[Config] = [
                Config(params=["test_command", "hello"], output="hello"),
            ]

            for config in configs:
                _get_cleaned_args.return_value = config.params
                cli.run()
                print_mock.assert_called_with(config.output)
                print_mock.reset_mock()

    @patch("targ.CLI._get_cleaned_args")
    def test_traceback(self, _get_cleaned_args: MagicMock):
        """
        Make sure the --trace option works.
        """

        def test_command():
            print("Command called")

        def test_exception():
            raise Exception("Bad things")

        cli = CLI()
        cli.register(test_command)
        cli.register(test_exception)

        with patch("builtins.print", side_effect=print_) as print_mock:

            # Make sure commands work as usual if no exceptions are raised.
            config = Config(
                params=["test_command", "--trace"], output="Command called"
            )
            _get_cleaned_args.return_value = config.params
            cli.run()
            print_mock.assert_called_with(config.output)
            print_mock.reset_mock()

            # Make sure a traceback is shown if an exception is raised.
            with patch("targ.traceback.format_exc") as traceback_mock:
                with self.assertRaises(SystemExit):
                    _get_cleaned_args.return_value = [
                        "test_exception",
                        "--trace",
                    ]
                    cli.run()
                    traceback_mock.assert_called_once()
