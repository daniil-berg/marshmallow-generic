from collections.abc import Callable
from typing import Any, Optional, TypeVar, overload
from typing_extensions import ParamSpec

from marshmallow.decorators import post_load as _post_load

_R = TypeVar("_R")
_P = ParamSpec("_P")


@overload
def post_load(
    fn: Callable[_P, _R],
    pass_many: bool = False,
    pass_original: bool = False,
) -> Callable[_P, _R]:
    ...


@overload
def post_load(
    fn: None = None,
    pass_many: bool = False,
    pass_original: bool = False,
) -> Callable[[Callable[_P, _R]], Callable[_P, _R]]:
    ...


def post_load(
    fn: Optional[Callable[..., Any]] = None,
    pass_many: bool = False,
    pass_original: bool = False,
) -> Callable[..., Any]:
    """
    Typed overload of the original `marshmallow.post_load` decorator function.

    Generic to ensure that the decorated function retains its type.
    Runtime behavior is unchanged.
    """
    return _post_load(fn, pass_many=pass_many, pass_original=pass_original)
