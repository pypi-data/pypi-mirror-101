import sys
from colorama import Fore, Back


def mate_print(data):
    if isinstance(data, dict):
        print()
        for key in data:
            print(magenta(str(key)) + " " + str(data[key]))
        print()
    elif isinstance(data, str):
        print(data)
    elif isinstance(data, list):
        print()
        for ele in data:
            print(magenta(str(ele)))
        print()
    return True


def yellow_background(s: str) -> str:  # pragma: no cover
    """Yellow color string if tty

    Args:
        s (str): String to color

    Returns:
        str: Colored string
    """
    if sys.stdout.isatty():
        return Back.YELLOW + Fore.BLACK + s + Fore.RESET + Back.RESET
    else:
        return s


def red(s: str) -> str:  # pragma: no cover
    """Red color string if tty

    Args:
        s (str): String to color

    Returns:
        str: Colored string
    """
    if sys.stdout.isatty():
        return Fore.RED + s + Fore.RESET
    else:
        return s


def blue(s: str) -> str:  # pragma: no cover
    """Blue color string if tty

    Args:
        s (str): String to color

    Returns:
        str: Colored string
    """
    if sys.stdout.isatty():
        return Fore.BLUE + s + Fore.RESET
    else:
        return s


def cyan(s: str) -> str:  # pragma: no cover
    """Cyan color string if tty

    Args:
        s (str): String to color

    Returns:
        str: Colored string
    """
    if sys.stdout.isatty():
        return Fore.CYAN + s + Fore.RESET
    else:
        return s


def green(s: str) -> str:  # pragma: no cover
    """Green color string if tty

    Args:
        s (str): String to color

    Returns:
        str: Colored string
    """
    if sys.stdout.isatty():
        return Fore.GREEN + s + Fore.RESET
    else:
        return s


def yellow(s: str) -> str:  # pragma: no cover
    """Yellow color string if tty

    Args:
        s (str): String to color

    Returns:
        str: Colored string
    """
    if sys.stdout.isatty():
        return Fore.YELLOW + s + Fore.RESET
    else:
        return s


def magenta(s: str) -> str:  # pragma: no cover
    """Magenta color string if tty

    Args:
        s (str): String to color

    Returns:
        str: Colored string
    """
    if sys.stdout.isatty():
        return Fore.MAGENTA + s + Fore.RESET
    else:
        return s
