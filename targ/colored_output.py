from __future__ import annotations
from enum import Enum

import colorama


colorama.init()


class Color(Enum):
    white = colorama.Fore.WHITE
    yellow = colorama.Fore.YELLOW
    red = colorama.Fore.RED


def print_colored(message: str, color: Color = Color.white, bold=False):
    colored_message = (
        (colorama.Style.BRIGHT if bold else "")
        + color.value
        + message
        + colorama.Fore.RESET
        + colorama.Style.RESET_ALL
    )
    print(colored_message)
