"""
Typed overloads for the [`marshmallow.decorators`][marshmallow.decorators] module.

Implements decorators as generic in terms of the decorated method types.
"""

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
    Register a method to invoke after deserializing an object.

    Typed overload of the original [`marshmallow.post_load`]
    [marshmallow.post_load] decorator function.
    Generic to ensure that the decorated function retains its type.
    Runtime behavior is unchanged.

    Receives the deserialized data and returns the processed data.
    By default it receives a single object at a time, transparently handling
    the `many` argument passed to the [`Schema.load`][marshmallow.Schema.load]
    call.

    Args:
        fn (Optional[Callable[P, R]]):
            The function to decorate or `None`; if a function is supplied,
            a decorated version of it is returned; if `None` the decorator
            is returned with its other arguments already bound.
        pass_many:
            If `True`, the raw data (which may be a collection) is passed
        pass_original:
            If `True`, the original data (before deserializing) will be passed
            as an additional argument to the method

    Returns:
        (Callable[P, R]): if `fn` is passed a function
        (Callable[[Callable[P, R]], Callable[P, R]]): if `fn` is `None`
    """
    return _post_load(fn, pass_many=pass_many, pass_original=pass_original)
