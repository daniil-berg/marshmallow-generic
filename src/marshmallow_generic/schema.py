"""
Definition of the `GenericSchema` base class.

For details about the inherited methods and attributes, see the official
documentation of [`marshmallow.Schema`][marshmallow.Schema].
"""

from collections.abc import Iterable, Mapping, Sequence
from typing import TYPE_CHECKING, Any, Literal, Optional, TypeVar, Union, overload

from marshmallow import Schema

from ._util import GenericInsightMixin
from .decorators import post_load

Model = TypeVar("Model")


class GenericSchema(GenericInsightMixin[Model], Schema):
    """
    Generic schema parameterized by a **`Model`** class.

    Data will always be deserialized to instances of that **`Model`** class.

    !!! note
        The **`Model`** referred to throughout the documentation is a
        **type variable**, not any concrete class. For more information about
        type variables, see the "Generics" section in
        [PEP 484](https://peps.python.org/pep-0484/#generics).

    Registers a `post_load` hook to pass validated data to the constructor
    of the specified **`Model`**.

    Requires a specific (non-generic) class to be passed as the **`Model`**
    type argument for deserialization to work properly:

    ```python
    class Foo:  # Model
        ...

    class FooSchema(GenericSchema[Foo]):
        ...
    ```
    """

    @post_load
    def instantiate(self, data: dict[str, Any], **_kwargs: Any) -> Model:
        """
        Unpacks `data` into the constructor of the specified **`Model`**.

        Registered as a [`@post_load`]
        [marshmallow_generic.decorators.post_load] hook for the schema.

        !!! warning
            You should probably **not** use this method directly;
            no parsing, transformation or validation of any kind is done
            in this method. The `data` passed to the **`Model`** constructor
            "as is".

        Args:
            data:
                The validated data after deserialization; will be unpacked
                into the constructor of the specified **`Model`** class.

        Returns:
            Instance of the schema's **`Model`** initialized with `**data`
        """
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
        ) -> list[Model]:
            ...

        @overload
        def load(
            self,
            data: Union[Mapping[str, Any], Iterable[Mapping[str, Any]]],
            *,
            many: Optional[Literal[False]] = None,
            partial: Union[bool, Sequence[str], set[str], None] = None,
            unknown: Optional[str] = None,
        ) -> Model:
            ...

        def load(
            self,
            data: Union[Mapping[str, Any], Iterable[Mapping[str, Any]]],
            *,
            many: Optional[bool] = None,
            partial: Union[bool, Sequence[str], set[str], None] = None,
            unknown: Optional[str] = None,
        ) -> Union[list[Model], Model]:
            """
            Deserializes data to objects of the specified **`Model`** class.

            Same as [`marshmallow.Schema.load`]
            [marshmallow.schema.Schema.load] at runtime, but data will always
            pass through the [`instantiate`]
            [marshmallow_generic.schema.GenericSchema.instantiate]
            hook after deserialization.

            Annotations ensure that type checkers will infer the return type
            correctly based on the **`Model`** type argument of the class.

            Args:
                data:
                    The data to deserialize
                many:
                    Whether to deserialize `data` as a collection. If `None`,
                    the value for `self.many` is used.
                partial:
                    Whether to ignore missing fields and not require any
                    fields declared. Propagates down to [`Nested`]
                    [marshmallow.fields.Nested] fields as well. If its value
                    is an iterable, only missing fields listed in that
                    iterable will be ignored. Use dot delimiters to specify
                    nested fields.
                unknown:
                    Whether to exclude, include, or raise an error for unknown
                    fields in the data. Use `EXCLUDE`, `INCLUDE` or `RAISE`.
                    If `None`, the value for `self.unknown` is used.

            Returns:
                (Model): if `many` is set to `False`
                (list[Model]): if `many` is set to `True`
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
        ) -> list[Model]:
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
        ) -> Model:
            ...

        def loads(
            self,
            json_data: str,
            *,
            many: Optional[bool] = None,
            partial: Union[bool, Sequence[str], set[str], None] = None,
            unknown: Optional[str] = None,
            **kwargs: Any,
        ) -> Union[list[Model], Model]:
            """
            Deserializes data to objects of the specified **`Model`** class.

            Same as [`marshmallow.Schema.loads`]
            [marshmallow.schema.Schema.loads] at runtime, but data will always
            pass through the [`instantiate`]
            [marshmallow_generic.schema.GenericSchema.instantiate]
            hook after deserialization.

            Annotations ensure that type checkers will infer the return type
            correctly based on the **`Model`** type argument of the class.

            Args:
                json_data:
                    A JSON string of the data to deserialize
                many:
                    Whether to deserialize `data` as a collection. If `None`,
                    the value for `self.many` is used.
                partial:
                    Whether to ignore missing fields and not require any
                    fields declared. Propagates down to [`Nested`]
                    [marshmallow.fields.Nested] fields as well. If its value
                    is an iterable, only missing fields listed in that
                    iterable will be ignored. Use dot delimiters to specify
                    nested fields.
                unknown:
                    Whether to exclude, include, or raise an error for unknown
                    fields in the data. Use `EXCLUDE`, `INCLUDE` or `RAISE`.
                    If `None`, the value for `self.unknown` is used.
                **kwargs:
                    Passed to the JSON decoder

            Returns:
                (Model): if `many` is set to `False`
                (list[Model]): if `many` is set to `True`
            """
            ...
