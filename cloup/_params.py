from __future__ import annotations

import inspect
from collections.abc import Sequence
from gettext import gettext as _
from typing import Any
from typing import Callable
from typing import TYPE_CHECKING
from typing import TypeVar
from typing import Union

import click
from click.decorators import _param_memo
from click.formatting import join_options
from click.types import _NumberRangeBase

if TYPE_CHECKING:
    from click.parser import OptionParser
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
    :param show_default: show the default value for this argument in its help text. Values are not shown by default,
                         unless :attr:`Context.show_default` is ``True``. If this value is a string, it shows that
                         string in parentheses instead of the actual value. This is particularly useful for
                         dynamic options
    """
    def __init__(
        self,
        *args: Any,
        help: str | None = None,
        hidden: bool | None = None,
        show_default: bool | str | None = None,
        **attrs: Any
    ):
        super().__init__(*args, **attrs)
        self.help = help
        self.hidden = hidden
        self.show_default = show_default

    def get_help_record(self, ctx: Context) -> tuple[str, str]:
        """
        Get data to output in help text

        This is implemented to allow the `show_default` option for arguments (similar to options). The code here is
        mostly pulled from :class:`click.Option.get_help_record`

        :param ctx: :class:`click.Context`
        """
        any_prefix_is_slash = False

        def _write_opts(opts: Sequence[str]) -> str:
            nonlocal any_prefix_is_slash
            rv, any_slashes = join_options(opts)
            if any_slashes:
                any_prefix_is_slash = True
            rv += f' {self.make_metavar()}'
            return rv

        rv = [_write_opts(self.opts)]
        if self.secondary_opts:
            rv.append(_write_opts(self.secondary_opts))

        help = self.help or ''
        extra: list[str] = []

        # Temporarily enable resilient parsing to avoid type casting failing for the default
        resilient = ctx.resilient_parsing
        ctx.resilient_parsing = True

        # Retrieve default value
        try:
            default_value = self.get_default(ctx, call=False)
        finally:
            ctx.resilient_parsing = resilient

        # Determine if we should show the default value
        show_default = False
        show_default_is_str = False

        if self.show_default is not None:
            if isinstance(self.show_default, str):
                show_default_is_str = show_default = True
            else:
                show_default = self.show_default
        elif ctx.show_default is not None:
            show_default = ctx.show_default

        # Add default info to help text extras
        if show_default_is_str or (show_default and (default_value is not None)):
            if show_default_is_str:
                default_string = f'({self.show_default})'
            elif isinstance(default_value, (list, tuple)):
                default_string = ', '.join(str(d) for d in default_value)
            elif inspect.isfunction(default_value):
                default_string = _('(dynamic)')
            else:
                default_string = str(default_value)

            if default_string:
                extra.append(_(f'default: {default_string}'))

        # Include description of value range if type is a range of numbers
        if (
            isinstance(self.type, _NumberRangeBase)
            # skip count with default range type
            and not (self.type.min == 0 and self.type.max is None)
        ):
            range_str = self.type._describe_range()
            if range_str:
                extra.append(range_str)

        # If not required, tag as "optional" (opposite of options)
        if not self.required:
            extra.append(_('optional'))

        # Add extra tags
        if extra:
            extra_str = '; '.join(extra)
            help = f'{help}  [{extra_str}]' if help else f'[{extra_str}]'

        return ('; ' if any_prefix_is_slash else ' / ').join(rv), help


class Option(click.Option):
    """
    A :class:`click.Option` with an extra field ``group`` of type ``OptionGroup``.

    :param nargs: same as base implementation, but additionally accepts `nargs=-1`, which mimics the behavior of
                  argparse `nargs='+'` (consume all items up until next option)
    """
    def __init__(self, *args: Any, group: OptionGroup | None = None, **attrs: Any):

        # Grab nargs and determine if we are consuming an arbitrary number
        nargs = attrs.get('nargs')
        if nargs is not None:
            self._consume_arbitrary_nargs = nargs == -1
        else:
            self._consume_arbitrary_nargs = False

        if nargs == -1:
            attrs.pop('nargs', None)

        super().__init__(*args, **attrs)
        self.group = group

        self._previous_parser_process = None
        self._eat_all_parser = None

    def add_to_parser(self, parser: OptionParser, ctx: Context) -> None:
        """
        Implemented to support `nargs=-1` for options

        Idea pulled from https://stackoverflow.com/a/48394004
        """
        def parser_process(value, state):
            nonlocal self
            if self._consume_arbitrary_nargs:
                done = False
                value = [value]

                # Grab everything up to the next option¡
                while state.rargs and not done:
                    for prefix in self._eat_all_parser.prefixes:
                        if state.rargs[0].startswith(prefix):
                            done = True
                    if not done:
                        value.append(state.rargs.pop(0))

                value = tuple(value)

            # Call the actual process
            self._previous_parser_process(value, state)

        super().add_to_parser(parser, ctx)
        for name in self.opts:
            our_parser = parser._long_opt.get(name) or parser._short_opt.get(name)
            if our_parser:
                self._eat_all_parser = our_parser
                self._previous_parser_process = our_parser.process
                our_parser.process = parser_process
                break


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
