"""Definition of the `GenericSchema` base class."""

from collections.abc import Iterable, Mapping, Sequence
from typing import TYPE_CHECKING, Any, Literal, Optional, TypeVar, Union, overload

from marshmallow import Schema

from ._util import GenericInsightMixin
from .decorators import post_load

_T = TypeVar("_T")


class GenericSchema(GenericInsightMixin[_T], Schema):
    """
    Schema parameterized by the class it deserializes data to.

    Registers a `post_load` hook to pass validated data to the constructor
    of the specified class.

    Requires a specific (non-generic) class to be passed as the type argument
    for deserialization to work properly.
    """

    @post_load
    def instantiate(self, data: dict[str, Any], **_kwargs: Any) -> _T:
        """Unpacks `data` into the constructor of the specified type."""
        return self._get_type_arg()(**data)

    if TYPE_CHECKING:

        @overload  # type: ignore[override]
        def load(
            self,
            data: Union[Mapping[str, Any], Iterable[Mapping[str, Any]]],
            *,
            many: Literal[True],
            partial: Union[bool, Sequence[str], set[str], None] = None,
            unknown: Optional[str] = None,
        ) -> list[_T]:
            ...

        @overload
        def load(
            self,
            data: Union[Mapping[str, Any], Iterable[Mapping[str, Any]]],
            *,
            many: Optional[Literal[False]] = None,
            partial: Union[bool, Sequence[str], set[str], None] = None,
            unknown: Optional[str] = None,
        ) -> _T:
            ...

        def load(
            self,
            data: Union[Mapping[str, Any], Iterable[Mapping[str, Any]]],
            *,
            many: Optional[bool] = None,
            partial: Union[bool, Sequence[str], set[str], None] = None,
            unknown: Optional[str] = None,
        ) -> Union[list[_T], _T]:
            """
            Same as `marshmallow.Schema.load` at runtime.

            Annotations ensure that type checkers will infer the return type
            correctly based on the type argument passed to a specific subclass.
            """
            ...

        @overload  # type: ignore[override]
        def loads(
            self,
            json_data: str,
            *,
            many: Literal[True],
            partial: Union[bool, Sequence[str], set[str], None] = None,
            unknown: Optional[str] = None,
            **kwargs: Any,
        ) -> list[_T]:
            ...

        @overload
        def loads(
            self,
            json_data: str,
            *,
            many: Optional[Literal[False]] = None,
            partial: Union[bool, Sequence[str], set[str], None] = None,
            unknown: Optional[str] = None,
            **kwargs: Any,
        ) -> _T:
            ...

        def loads(
            self,
            json_data: str,
            *,
            many: Optional[bool] = None,
            partial: Union[bool, Sequence[str], set[str], None] = None,
            unknown: Optional[str] = None,
            **kwargs: Any,
        ) -> Union[list[_T], _T]:
            """
            Same as `marshmallow.Schema.loads` at runtime.

            Annotations ensure that type checkers will infer the return type
            correctly based on the type argument passed to a specific subclass.
            """
            ...
