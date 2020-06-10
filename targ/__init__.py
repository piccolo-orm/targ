from __future__ import annotations
import asyncio
from dataclasses import dataclass, field
import inspect
import json
import sys
import traceback
import typing as t

from docstring_parser import parse, Docstring, DocstringParam

from .format import Color, format_text, get_underline


__VERSION__ = "0.1.6"


@dataclass
class Arguments:
    args: t.List[str] = field(default_factory=list)
    kwargs: t.Dict[str, t.Any] = field(default_factory=dict)


@dataclass
class Command:
    command: t.Callable
    group_name: t.Optional[str] = None
    command_name: t.Optional[str] = None

    def __post_init__(self):
        self.command_docstring: Docstring = parse(self.command.__doc__)
        self.annotations = t.get_type_hints(self.command)
        self.signature = inspect.signature(self.command)
        if not self.command_name:
            self.command_name = self.command.__name__

    @property
    def full_name(self):
        return (
            f"{self.group_name} {self.command_name}"
            if self.group_name
            else self.command_name
        )

    @property
    def description(self) -> str:
        docstring: Docstring = parse(self.command.__doc__)
        return " ".join(
            [
                docstring.short_description or "",
                docstring.long_description or "",
            ]
        )

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

    @property
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
            if arg_description:
                output.append(arg_description)
            output.append("")

        return "\n".join(output)

    @property
    def usage(self) -> str:
        """
        Example:

        some_command required_arg [--optional_arg=value] [--some_flag]
        """
        output = [format_text(self.command_name or "", color=Color.green)]

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

    def print_help(self):
        print("")
        print(self.command_name)
        print(get_underline(len(self.command_name)))
        print(self.description)

        print("")
        print("Usage")
        print(get_underline(5, character="-"))
        print(self.usage)
        print("")

        print("Args")
        print(get_underline(4, character="-"))
        if self.arguments_description:
            print(self.arguments_description)
        else:
            print("No args")
        print("")

    def call_with(self, arg_class: Arguments):
        """
        Call the command function with the given arguments.
        """
        if arg_class.kwargs.get("help"):
            self.print_help()
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

        if inspect.iscoroutinefunction(self.command):
            asyncio.run(self.command(**kwargs))
        else:
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

    @property
    def group_names(self) -> t.List[str]:
        return [i.group_name for i in self.commands if i.group_name]

    def command_exists(self, group_name: str, command_name: str) -> bool:
        for command in self.commands:
            if (
                command.group_name == group_name
                and command.command_name == command_name
            ):
                return True
        return False

    def _validate_group_name(self, group_name: str) -> bool:
        if " " in group_name:
            return False
        return True

    def register(
        self,
        command: t.Callable,
        group_name: t.Optional[str] = None,
        command_name: t.Optional[str] = None,
    ):
        if group_name and not self._validate_group_name(group_name):
            raise ValueError("The group name should not contain spaces.")

        self.commands.append(
            Command(
                command=command,
                group_name=group_name,
                command_name=command_name,
            )
        )

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
            lines.append(format_text(command.full_name, color=Color.green))
            lines.append(command.description)
            lines.append("")

        return "\n".join(lines)

    def get_cleaned_args(self) -> t.List[str]:
        """
        Remove any redundant arguments.
        """
        return sys.argv[1:]

    def get_command(
        self, command_name: str, group_name: t.Optional[str] = None
    ) -> t.Optional[Command]:
        for command in self.commands:
            if command.command_name == command_name:
                if group_name and command.group_name != group_name:
                    continue
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
        cleaned_args = self.get_cleaned_args()

        if len(cleaned_args) == 0:
            print(self.get_help_text())
            return

        command_name = cleaned_args[0]

        command = self.get_command(command_name=command_name)

        if command:
            cleaned_args = cleaned_args[1:]
        else:
            # See if it belongs to a group:
            if len(cleaned_args) >= 2:
                group_name = cleaned_args[0]
                command_name = cleaned_args[1]
                command = self.get_command(
                    command_name=command_name, group_name=group_name
                )
                if command:
                    cleaned_args = cleaned_args[2:]

        if not command:
            print(f"Unrecognised command - {command_name}")
            print(self.get_help_text())
        else:
            try:
                arg_class = self.get_arg_class(cleaned_args)
                command.call_with(arg_class)
            except Exception as exception:
                print(format_text("The command failed.", color=Color.red))
                print(exception)

                if "--trace" in cleaned_args:
                    print(traceback.format_exc())

                command.print_help()
                sys.exit(1)
