"""
Parameter types and "shortcuts" for creating commonly used types.
"""
from __future__ import annotations

import pathlib
from collections.abc import Sequence
from datetime import datetime
from gettext import gettext as _
from typing import Any
from typing import cast
from typing import TYPE_CHECKING

import click
from click.types import Choice as _Choice
from click.types import DateTime as _DateTime
from click.types import ParamType
from click.types import Path

from cloup.typing import MISSING

if TYPE_CHECKING:
    from click import Context
    from click import Parameter


"""
Type shortcuts
"""


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


"""
Default type augmentations
"""


class Choice(_Choice):
    """
    The choice type allows a value to be checked against a fixed set of supported values.
    All of these values have to be strings.

    You should only pass a list or tuple of choices. Other iterables (like generators) may lead to surprising results.

    The resulting value will always be one of the originally passed choices regardless of ``case_sensitive`` or
    any ``ctx.token_normalize_func`` being specified.

    See :ref:`choice-opts` for an example.

    Implemented in connormason/cloup:
        - Support for usage with options with nargs=-1 (implemented in our custom Option class)

    :param choices: choices to provide as options
    :param case_sensitive: Set to false to make choices case insensitive. Defaults to true.
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
                        _(f'invalid choice: {value_item}. (choose from {", ".join(self.choices)})'),
                        param,
                        ctx
                    )
            else:
                return normed_value
        elif normed_value in normed_choices:
            return normed_choices[normed_value]
        else:
            return self.fail(_(f'invalid choice: {value}. (choose from {", ".join(self.choices)})'), param, ctx)


class DateTime(_DateTime):
    """
    The DateTime type converts date strings into `datetime` objects.

    The format strings which are checked are configurable, but default to some common (non-timezone aware)
    ISO 8601 formats.

    When specifying *DateTime* formats, you should only pass a list or a tuple. Other iterables, like generators, may
    lead to surprising results.

    The format strings are processed using ``datetime.strptime``, and this consequently defines the format strings
    which are allowed.

    Parsing is tried using each format, in order, and the first format which parses successfully is used.

    Implemented in connormason/cloup:
        - Added ``formats_in_metavar`` kwarg
        - Added ``use_dateutil`` kwarg

    :param formats: a list or tuple of date format strings, in the order in which they should be tried. Defaults to
                    ``'%Y-%m-%d'``, ``'%Y-%m-%dT%H:%M:%S'``, ``'%Y-%m-%d %H:%M:%S'``.
    :param formats_in_metavar: if True, datetime formats will be shown as the option metavar. If False, "DATETIME" will
                               be shown as the option metavar
    :param use_dateutil: if True, python-dateutil will be used to parse the option value. When True, the ``formats``
                         kwarg is ignored. If `python-dateutil` is not installed, an ImportError will be raised
    """
    def __init__(
        self,
        formats: Sequence[str] | None = None,
        formats_in_metavar: bool = True,
        use_dateutil: bool = False
    ):
        super().__init__(formats=formats)
        self.formats_in_metavar = formats_in_metavar
        self.use_dateutil = use_dateutil

    def to_info_dict(self) -> dict[str, Any]:
        info_dict = super().to_info_dict()
        info_dict['use_dateutil'] = self.use_dateutil
        return info_dict

    def get_metavar(self, param: Parameter) -> str:
        if self.formats_in_metavar and not self.use_dateutil:
            return f'[{" | ".join(self.formats)}]'
        else:
            return 'DATETIME'

    def convert(self, value: Any, param: Parameter | None, ctx: Context | None) -> Any:
        if isinstance(value, datetime):
            return value

        if self.use_dateutil:
            try:
                from dateutil.parser import parse as parse_datetime
            except (ModuleNotFoundError, ImportError, NameError) as e:
                raise ImportError('python-dateutil must be installed to use_dateutil with click.DateTime') from e
            else:
                from dateutil.parser import ParserError
                try:
                    return parse_datetime(value)
                except ParserError:
                    self.fail(_(f'{value} is not a valid datetime'), param, ctx)

        else:
            return super().convert(value, param, ctx)


"""
Custom types
"""


class Integer(ParamType):
    """
    Integer parameter type. Same as providing `type=int` to a parameter, but adds some additional functionality

    Implemented in connormason/cloup:
        - Added `base` kwarg
        - Added `as_str` kwargs

    :param base: base of integer to parse as (as accepted by the `base` arg of :func:`int`)
    :param as_str: if True, value will be validated then returned as string (instead of being converted to an int)
    """
    def __init__(self, base: int = 10, as_str: bool = False):
        self.base = base
        self.as_str = as_str

    def convert(self, value: Any, param: Parameter | None, ctx: Context | None) -> Any:
        try:
            converted_value = int(value, self.base)
        except ValueError:
            self.fail(_(f'{repr(value)} is not a valid integer'), param, ctx)
        else:
            return value if self.as_str else converted_value


class JSON(ParamType):
    """
    Parameter type that expects valid JSON and returns the parsed JSON

    :param type: require that parsed JSON must be an instance of a specific type (list, dict, etc)
    :param str_ok: if True, parameter value can be a str representation of JSON
    :param path_ok: if True, parameter value can be a path to a JSON file
    """
    name = 'json'

    def __init__(
        self,
        type: type | None = None,
        str_ok: bool = True,
        path_ok: bool = False,
    ):
        self.type = type
        self.str_ok = str_ok
        self.path_ok = path_ok

    def convert(self, value: str, param: click.Parameter | None, ctx: click.Context | None) -> object:
        import json

        val: Any = MISSING
        path_exc: Exception | None = None

        if self.path_ok:
            path_param_type = Path(exists=True, dir_okay=False, path_type=pathlib.Path)
            try:
                _path = path_param_type.convert(value, param, ctx)
            except click.BadParameter as exc:
                path_exc = exc
            else:
                _path = cast(pathlib.Path, _path)
                try:
                    with _path.open() as f:
                        val = json.load(f)
                except json.JSONDecodeError as e:
                    self.fail(_(f'Path {_path} contains invalid JSON. {str(e)}'), param, ctx)

        if self.str_ok and (val is MISSING):
            try:
                val = json.loads(value)
            except json.JSONDecodeError as e:
                if (path_exc is not None) and ('line 1 column 1 (char 0)' in str(e)):
                    self.fail(_(str(path_exc)), param, ctx)
                else:
                    self.fail(_(f'Invalid JSON provided. {str(e)}'), param, ctx)

        if (self.type is not None) and (not isinstance(val, self.type)):
            self.fail(_(f'Provided JSON must be of type "{self.type}"'), param, ctx)
            return None     # This is here to appease mypy
        else:
            return val


class JSONString(JSON):
    """
    Parameter type that expects a valid JSON str and returns the parsed JSON

    :param type: require that parsed JSON must be an instance of a specific type (list, dict, etc)
    """
    def __init__(self, type: type | None = None):
        super().__init__(type=type, path_ok=False)


class JSONPath(JSON):
    """
    Parameter type that expects a valid JSON file and returns the parsed JSON

    :param type: require that parsed JSON must be an instance of a specific type (list, dict, etc)
    """
    def __init__(self, type: type | None = None):
        super().__init__(type=type, str_ok=False)
