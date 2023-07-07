"""
Parameter types and "shortcuts" for creating commonly used types.
"""
from __future__ import annotations

import pathlib
from typing import Any
from typing import TYPE_CHECKING

import click
from click.types import Choice as _Choice

if TYPE_CHECKING:
    from click import Context
    from click import Parameter


def path(
    *,
    path_type: type = pathlib.Path,
    exists: bool = False,
    file_okay: bool = True,
    dir_okay: bool = True,
    writable: bool = False,
    readable: bool = True,
    resolve_path: bool = False,
    allow_dash: bool = False,
) -> click.Path:
    """
    Shortcut for :class:`click.Path` with ``path_type=pathlib.Path``.
    """
    return click.Path(**locals())


def dir_path(
    *,
    path_type: type = pathlib.Path,
    exists: bool = False,
    writable: bool = False,
    readable: bool = True,
    resolve_path: bool = False,
    allow_dash: bool = False,
) -> click.Path:
    """
    Shortcut for :class:`click.Path` with ``file_okay=False, path_type=pathlib.Path``.
    """
    return click.Path(**locals(), file_okay=False)


def file_path(
    *,
    path_type: type = pathlib.Path,
    exists: bool = False,
    writable: bool = False,
    readable: bool = True,
    resolve_path: bool = False,
    allow_dash: bool = False,
) -> click.Path:
    """
    Shortcut for :class:`click.Path` with ``dir_okay=False, path_type=pathlib.Path``.
    """
    return click.Path(**locals(), dir_okay=False)


class Choice(_Choice):
    """
    Same as :class:`click.types.Choice`, but supports nargs=-1 for options
    """
    def convert(self, value: Any, param: Parameter | None, ctx: Context | None) -> str:
        normed_value = value
        normed_choices = {choice: choice for choice in self.choices}

        consume_arbitrary_args = hasattr(param, '_consume_arbitrary_nargs')
        consume_arbitrary_args = consume_arbitrary_args and param._consume_arbitrary_nargs  # type: ignore

        if (ctx is not None) and (ctx.token_normalize_func is not None):
            normed_value = ctx.token_normalize_func(value)
            normed_choices = {
                ctx.token_normalize_func(normed_choice): original
                for normed_choice, original in normed_choices.items()
            }

        if not self.case_sensitive:  # type: ignore
            if consume_arbitrary_args:
                normed_value = tuple(str.casefold(value) for value in normed_value)
            else:
                normed_value = str.casefold(normed_value)

            normed_choices = {
                str.casefold(normed_choice): original
                for normed_choice, original in normed_choices.items()
            }

        if consume_arbitrary_args:
            for value_item in normed_value:
                if value_item not in normed_choices:
                    return self.fail(
                        f'invalid choice: {value_item}. (choose from {", ".join(self.choices)})', param, ctx
                    )
            else:
                return normed_value
        elif normed_value in normed_choices:
            return normed_choices[normed_value]
        else:
            return self.fail(f'invalid choice: {value}. (choose from {", ".join(self.choices)})', param, ctx)
