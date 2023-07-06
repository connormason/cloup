"""
Constraints for parameter groups.

.. versionadded:: v0.5.0
"""
from __future__ import annotations

from ._conditional import If
from ._core import accept_none
from ._core import AcceptAtMost
from ._core import AcceptBetween
from ._core import all_or_none
from ._core import And
from ._core import Constraint
from ._core import ErrorFmt
from ._core import ErrorRephraser
from ._core import HelpRephraser
from ._core import mutually_exclusive
from ._core import Operator
from ._core import Or
from ._core import Rephraser
from ._core import require_all
from ._core import require_any
from ._core import require_one
from ._core import RequireAtLeast
from ._core import RequireExactly
from ._core import WrapperConstraint
from ._support import BoundConstraintSpec
from ._support import constrained_params
from ._support import constraint
from ._support import ConstraintMixin
from .conditions import AllSet
from .conditions import AnySet
from .conditions import Equal
from .conditions import IsSet
from .conditions import Not
from .exceptions import ConstraintViolated
from .exceptions import UnsatisfiableConstraint

__all__ = [
    'AcceptAtMost',
    'AcceptBetween',
    'AllSet',
    'And',
    'AnySet',
    'BoundConstraintSpec',
    'Constraint',
    'ConstraintMixin',
    'ConstraintViolated',
    'Equal',
    'ErrorFmt',
    'ErrorRephraser',
    'HelpRephraser',
    'If',
    'IsSet',
    'Not',
    'Operator',
    'Or',
    'Rephraser',
    'RequireAtLeast',
    'RequireExactly',
    'UnsatisfiableConstraint',
    'WrapperConstraint',
    'accept_none',
    'all_or_none',
    'constrained_params',
    'constraint',
    'mutually_exclusive',
    'require_all',
    'require_any',
    'require_one',
]
