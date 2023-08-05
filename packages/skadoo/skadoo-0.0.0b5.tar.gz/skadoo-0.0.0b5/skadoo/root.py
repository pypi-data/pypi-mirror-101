from typing import NamedTuple, Dict, List

from skadoo.flags import Flag
from skadoo import utils


class Root(NamedTuple):
    """
    Root argument object.

    Attributes:
        name (string): Name of argument.
        description (string): Description of argument.
        called (bool): Boolean of if the argument is called. Defaults to False.
        flags (dict): Dictionary of Flags for Root with. Defaults to [].
    """

    name: str
    root: str
    description: str
    called: bool
    flags: Dict[str, Flag]


def create_root(name: str, description: str = "", flags: List[Flag] = []) -> Root:
    """
    Create a Root argument.

    Args:
        name (str): Name of argument.
        description (str, optional): Description of argument. Defaults to "".
        flags (list-like): Flag args used by Root arg. Defaults to {}.

    Returns:
        Root
    """
    root = "_".join(utils.get_name_parts(name))

    called = utils.is_called(root)

    return Root(name, root, description, called, flags={_.name: _ for _ in flags})
