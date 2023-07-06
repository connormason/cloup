from __future__ import annotations

from typing import Any
from typing import Callable
from typing import TYPE_CHECKING
from typing import TypeVar
from typing import Union

import click
from click.decorators import _param_memo

if TYPE_CHECKING:
    from cloup import Context
    from cloup._commands import Command
    from cloup._option_groups import OptionGroup


FC = TypeVar('FC', bound=Union[Callable[..., Any], 'Command'])


class Argument(click.Argument):
    """
    A :class:`click.Argument` with help text.

    :param help: help text shown next to argument
    :param hidden: hide this argument from help output. If the argument has no help text, it is hidden by default, and
                   setting this to True will show it. If the argument has help text, it is shown by default, and setting
                   this to False will hide it
    """
    def __init__(
        self,
        *args: Any,
        help: str | None = None,
        hidden: bool | None = None,
        **attrs: Any
    ):
        super().__init__(*args, **attrs)
        self.help = help
        self.hidden = hidden

    def get_help_record(self, ctx: Context) -> tuple[str, str]:
        return self.make_metavar(), self.help or ''


class Option(click.Option):
    """
    A :class:`click.Option` with an extra field ``group`` of type ``OptionGroup``.
    """
    def __init__(self, *args: Any, group: OptionGroup | None = None, **attrs: Any):
        super().__init__(*args, **attrs)
        self.group = group


GroupedOption = Option
"""Alias of ``Option``."""


def argument(
    *param_decls: str,
    cls: type[click.Argument] | None = None,
    **attrs: Any
) -> Callable[[FC], FC]:
    ArgumentClass = cls or Argument

    def decorator(f):
        _param_memo(f, ArgumentClass(param_decls, **attrs))
        return f

    return decorator


def option(
    *param_decls: str,
    cls: type[click.Option] | None = None,
    group: OptionGroup | None = None,
    **attrs: Any
) -> Callable[[FC], FC]:
    """
    Attach an ``Option`` to the command.
    Refer to :class:`click.Option` and :class:`click.Parameter` for more info
    about the accepted parameters.

    In your IDE, you won't see arguments relating to shell completion,
    because they are different in Click 7 and 8 (both supported by Cloup):

    - in Click 7, it's ``autocompletion``
    - in Click 8, it's ``shell_complete``.

    These arguments have different semantics, refer to Click's docs.
    """
    OptionClass = cls or Option

    def decorator(f):
        _param_memo(f, OptionClass(param_decls, **attrs))
        new_option = f.__click_params__[-1]
        new_option.group = group
        if group and group.hidden:
            new_option.hidden = True
        return f

    return decorator
