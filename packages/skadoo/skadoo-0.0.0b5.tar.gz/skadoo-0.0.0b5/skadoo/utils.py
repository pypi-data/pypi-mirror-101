import sys

from typing import List


def str_to_bool(string: str) -> bool:
    """
    Converts string to bool.

    Args:
        string (str): ("Yes", "No", "True", "False", "1", "0")

    Returns:
        bool
    """
    if isinstance(string, bool):
        return string

    if string is None:
        return False

    if string.lower() in ("yes", "true", "t", "y", "1"):
        return True

    elif string.lower() in ("no", "false", "f", "n", "0"):
        return False

    return False


def get_command_parts() -> List[str]:
    """
    Parse command line arguments and return cleaned for "=" flags.

    Returns:
        List[str]
    """
    clean_args = []
    for _ in sys.argv:
        clean_args += _.lower().split("=")

    return clean_args


def get_name_parts(name: str) -> List[str]:
    """
    Get name parts from name of argument for constructing internal arg name or 
    flag identity.

    Args:
        name (str): String of name for arugment (ex: "My Argument").

    Returns:
        List[str]
    """
    return (
        name.lower().replace("--", " ").strip().replace("-", " ").replace("_", " ").split(" ")
    )


def is_called(name: str, abbreviation: str = None) -> bool:
    """
    Checks if string is in sys.argv.

    Args:
        name (str): Full string to check for.
        abbreviation (str): Abbreviation to check for.

    Returns:
        bool
    """
    parts = get_command_parts()

    found = True if name in parts else False

    if abbreviation and not found:
        found = True if abbreviation in parts else False

    return found