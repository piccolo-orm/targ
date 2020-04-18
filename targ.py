from functools import cached_property
from sys import argv
from dataclasses import dataclass, field
import typing as t

from docstring_parser import parse, Docstring


__VERSION__ = "0.1.0"


@dataclass
class Arguments:
    args: t.List[str] = field(default_factory=list)
    kwargs: t.Dict[str, str] = field(default_factory=dict)


@dataclass
class Command:
    command: t.Callable

    @cached_property
    def description(self) -> str:
        docstring: Docstring = parse(self.command.__doc__)
        return f"{self.command.__name__} - {docstring.short_description}"

    def call_with(self, arg_class: Arguments):
        """
        Call the command function with the given arguments.
        """
        annotations = t.get_type_hints(self.command)

        kwargs = {}

        for kwarg_key, kwarg_value in arg_class.kwargs.items():
            annotation = annotations.get(kwarg_key)
            # This only works with basic types like str at the moment.
            if callable(annotation):
                kwargs[kwarg_key] = annotation(kwarg_value)

        for index, arg in enumerate(arg_class.args):
            kwarg_key, annotation = list(annotations.items())[index]
            if callable(annotation):
                kwargs[kwarg_key] = annotation(arg)

        self.command(**kwargs)


@dataclass
class CLI:
    """
    The root class for building the CLI.

    Example usage:

    cli = CLI()
    cli.register(some_function)
    """

    description: str = "Targ CLI"
    commands: t.List[Command] = field(default_factory=list)

    def register(self, command: t.Callable, group: t.Optional[str] = None):
        self.commands.append(Command(command))

    def get_help_text(self) -> str:
        return "\n".join(
            [self.description] + [i.description for i in self.commands]
        )

    def get_cleaned_args(self) -> t.List[str]:
        """
        Remove any redundant arguments.
        """
        output: t.List[str] = []
        for index, arg in enumerate(argv):
            if arg.endswith(".py") and index == 0:
                continue
            else:
                output.append(arg)
        return output

    def get_command(self, command_name: str) -> t.Optional[Command]:
        for command in self.commands:
            if command.command.__name__ == command_name:
                return command
        return None

    def get_arg_class(self, args: t.List[str]) -> Arguments:
        arguments = Arguments()
        for arg_str in args:
            if arg_str.startswith("--"):
                name, value = arg_str[2:].split("=", 1)
                arguments.kwargs[name] = value
            else:
                arguments.args.append(arg_str)
        return arguments

    def run(self):
        args = self.get_cleaned_args()

        if len(args) == 0:
            print(self.get_help_text())
            return

        command_name = args[0]
        args = args[1:]

        command = self.get_command(command_name=command_name)
        if not command:
            print(f"Unrecognised command - {command_name}")
            print(self.get_help_text())
        else:
            arg_class = self.get_arg_class(args)
            command.call_with(arg_class)
