from __future__ import annotations

from click import Argument
from click import Option

from cloup.constraints.common import format_param
from cloup.constraints.common import format_param_list
from cloup.constraints.common import get_param_label
from cloup.constraints.common import join_with_and
from cloup.constraints.common import param_value_is_set
from tests.util import bool_opt
from tests.util import flag_opt
from tests.util import int_opt
from tests.util import multi_opt
from tests.util import parametrize
from tests.util import tuple_opt


@parametrize(
    'param_type,    value,      expected',
    (Argument,      None,       False),
    (Argument,      'bu',       True),
    (Option,        None,       False),
    (Option,        'bu',       True),
    (int_opt,       0,          True),
    (bool_opt,      False,      True),   # non-flag boolean opts are set even if False
    (flag_opt,      False,      False),
    (flag_opt,      True,       True),
    (tuple_opt,     (),         False),
    (tuple_opt,     (1, 2),     True),
    (multi_opt,     (),         False),
    (multi_opt,     (1, 2),     True),
    ids=lambda val: val.__name__ if callable(val) else None,
)
def test_param_value_is_set(param_type, value, expected):
    param = param_type(['-o'])
    actual = param_value_is_set(param, value)
    assert actual == expected


def test_get_param_label():
    assert get_param_label(Argument(['arg'])) == 'ARG'
    assert get_param_label(Option(['--opt'])) == '--opt'
    assert get_param_label(Option(['--opt', '-o'])) == '--opt'
    assert get_param_label(Option(['-o', '--opt'])) == '--opt'
    assert get_param_label(Option(['-o/-O', '--opt/--no-opt'])) == '--opt'


def test_format_param():
    assert format_param(Argument(['arg'])) == 'ARG'
    assert format_param(Option(['--opt'])) == '--opt'
    assert format_param(Option(['-o'])) == '-o'
    assert format_param(Option(['--opt', '-o'])) == '--opt (-o)'
    assert format_param(Option(['-o', '--opt'])) == '--opt (-o)'
    assert format_param(Option(['-o/-O', '--opt/--no-opt', 'blah'])) == '--opt (-o)'


def test_format_param_list():
    params = [
        Argument(['arg']),
        Option(['--one']),
        Option(['--two', '-t']),
    ]
    expected = (' ARG\n'
                ' --one\n'
                ' --two (-t)\n')
    assert format_param_list(params, indent=1) == expected


def test_join_with_and():
    assert join_with_and([]) == ''
    assert join_with_and('A') == 'A'
    assert join_with_and('ABC', sep='; ') == 'A; B and C'
