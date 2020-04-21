from __future__ import annotations
from dataclasses import dataclass, field
from functools import cached_property
import inspect
import json
import sys
import typing as t

from docstring_parser import parse, Docstring, DocstringParam

from .format import (
    Color,
    format_text,
    get_underline,
)


__VERSION__ = "0.1.1"


@dataclass
class Arguments:
    args: t.List[str] = field(default_factory=list)
    kwargs: t.Dict[str, t.Any] = field(default_factory=dict)


@dataclass
class Command:
    command: t.Callable

    def __post_init__(self):
        self.command_docstring: Docstring = parse(self.command.__doc__)
        self.annotations = t.get_type_hints(self.command)
        self.signature = inspect.signature(self.command)

    @cached_property
    def description(self) -> str:
        docstring: Docstring = parse(self.command.__doc__)
        return docstring.short_description

    def _get_docstring_param(self, arg_name) -> t.Optional[DocstringParam]:
        for param in self.command_docstring.params:
            if param.arg_name == arg_name:
                return param
        return None

    def _get_arg_description(self, arg_name: str) -> str:
        docstring_param = self._get_docstring_param(arg_name)
        if docstring_param:
            return docstring_param.description
        else:
            return ""

    def _get_arg_default(self, arg_name: str):
        parameter = self.signature.parameters.get(arg_name)
        if parameter:
            default = parameter.default
            if default is not inspect._empty:  # type: ignore
                return default
        return None

    @cached_property
    def arguments_description(self) -> str:
        """
        :returns: A string containing a description for each argument.
        """
        output = []

        for arg_name, annotation in self.annotations.items():
            arg_description = self._get_arg_description(arg_name=arg_name)

            arg_default = self._get_arg_default(arg_name=arg_name)
            arg_default_json = json.dumps(arg_default)

            default_str = (
                f"[default={arg_default_json}]"
                if arg_default is not None
                else ""
            )

            output.append(
                format_text(arg_name, color=Color.cyan) + f" {default_str}"
            )
            output.append(arg_description)
            output.append("")

        return "\n".join(output)

    @cached_property
    def usage(self) -> str:
        """
        Example:

        some_command required_arg [--optional_arg=value] [--some_flag]
        """
        output = [format_text(self.command.__name__, color=Color.green)]

        for arg_name, parameter in self.signature.parameters.items():
            if parameter.default is inspect._empty:  # type: ignore
                output.append(format_text(arg_name, color=Color.cyan))
            else:
                if parameter.default is False:
                    output.append(
                        format_text(f"[--{arg_name}]", color=Color.cyan)
                    )
                else:
                    output.append(
                        format_text(f"[--{arg_name}=X]", color=Color.cyan)
                    )

        return " ".join(output)

    def call_with(self, arg_class: Arguments):
        """
        Call the command function with the given arguments.
        """
        if arg_class.kwargs.get("help"):
            name = self.command.__name__

            print("")
            print(name)
            print(get_underline(len(name)))
            print(self.description)

            print("")
            print("Usage")
            print(get_underline(5, character="-"))
            print(self.usage)
            print("")

            print("Args")
            print(get_underline(4, character="-"))
            print(self.arguments_description)
            print("")

            return

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
        lines = [
            "",
            self.description,
            get_underline(len(self.description)),
            (
                "Enter the name of a command followed by --help to learn "
                "more."
            ),
            "",
            "",
            "Commands",
            "--------",
        ]

        for command in self.commands:
            lines.append(
                format_text(command.command.__name__, color=Color.green)
            )
            lines.append(command.description)
            lines.append("")

        return "\n".join(lines)

    def get_cleaned_args(self) -> t.List[str]:
        """
        Remove any redundant arguments.
        """
        output: t.List[str] = []
        for index, arg in enumerate(sys.argv):
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

    def _clean_cli_argument(self, value: str) -> t.Any:
        if value in ["True", "true", "t"]:
            return True
        elif value in ["False", "false", "f"]:
            return False
        return value

    def get_arg_class(self, args: t.List[str]) -> Arguments:
        arguments = Arguments()
        for arg_str in args:
            if arg_str.startswith("--"):
                components = arg_str[2:].split("=", 1)
                if len(components) == 2:
                    # For value arguments, like --user=bob
                    name = components[0]
                    value = self._clean_cli_argument(components[1])
                else:
                    # For flags, like --verbose.
                    name = components[0]
                    value = True

                arguments.kwargs[name] = value
            else:
                value = self._clean_cli_argument(arg_str)
                arguments.args.append(value)
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
            try:
                arg_class = self.get_arg_class(args)
                command.call_with(arg_class)
            except Exception as exception:
                print(format_text("The command failed.", color=Color.red))
                print(exception)
                sys.exit(1)
