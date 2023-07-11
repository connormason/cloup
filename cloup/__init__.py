"""Top-level package for cloup."""
# WARNING: _version.py is generated by setuptools-scm upon package building/installation
from __future__ import annotations

from . import _version

__author__ = """Gianluca Gippetto"""
__email__ = 'gianluca.gippetto@gmail.com'
__version__ = _version.version
__version_tuple__ = _version.version_tuple

from click import (
    # decorators
    confirmation_option,
    help_option,
    pass_context,
    pass_obj,
    password_option,
    version_option,
    # types
    BOOL,
    DateTime,
    File,
    FLOAT,
    FloatRange,
    INT,
    IntRange,
    ParamType,
    Path,
    STRING,
    Tuple,
    UNPROCESSED,
    UUID,
)

from . import warnings
from .styling import (
    HelpTheme,
    Style,
    Color,
)
from .formatting import (
    HelpFormatter,
    HelpSection,
)
from ._context import Context
from ._params import Argument, Option, argument, option
from ._option_groups import (
    OptionGroup,
    OptionGroupMixin,
    option_group,
)
from ._sections import (
    Section,
    SectionMixin,
)
from ._commands import (
    Command,
    Group,
    command,
    group,
)
from .constraints import (
    ConstraintMixin,
    constrained_params,
    constraint,
)
from .types import dir_path, file_path, path, Choice

__all__ = [
    'Argument',
    'BOOL',
    'Choice',
    'Color',
    'Command',
    'ConstraintMixin',
    'Context',
    'DateTime',
    'FLOAT',
    'File',
    'FloatRange',
    'Group',
    'HelpFormatter',
    'HelpSection',
    'HelpTheme',
    'INT',
    'IntRange',
    'Option',
    'OptionGroup',
    'OptionGroupMixin',
    'ParamType',
    'Path',
    'STRING',
    'Section',
    'SectionMixin',
    'Style',
    'Tuple',
    'UNPROCESSED',
    'UUID',
    '_version',
    'argument',
    'command',
    'confirmation_option',
    'constrained_params',
    'constraint',
    'dir_path',
    'file_path',
    'group',
    'help_option',
    'option',
    'option_group',
    'pass_context',
    'pass_obj',
    'password_option',
    'path',
    'version_option',
    'warnings',
]
