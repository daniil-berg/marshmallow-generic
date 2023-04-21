"""
Definition of the `GenericSchema` base class.

For details about the inherited methods and attributes, see the official
documentation of [`marshmallow.Schema`][marshmallow.Schema].
"""

from collections.abc import Iterable, Mapping, Sequence
from typing import TYPE_CHECKING, Any, Literal, Optional, TypeVar, Union, overload
from warnings import warn

from marshmallow import Schema

from ._util import GenericInsightMixin1
from .decorators import post_load

Model = TypeVar("Model")

MANY_SCHEMA_UNSAFE = (
    "Changing `many` schema-wide breaks type safety. "
    "Use the the `many` parameter of specific methods (like `load`) instead."
)


class GenericSchema(GenericInsightMixin1[Model], Schema):
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

    def __init__(
        self,
        *,
        only: Union[Sequence[str], set[str], None] = None,
        exclude: Union[Sequence[str], set[str]] = (),
        context: Union[dict[str, Any], None] = None,
        load_only: Union[Sequence[str], set[str]] = (),
        dump_only: Union[Sequence[str], set[str]] = (),
        partial: Union[bool, Sequence[str], set[str]] = False,
        unknown: Optional[str] = None,
        many: bool = False,  # usage discouraged
    ) -> None:
        """
        Emits a warning, if the `many` argument is not `False`.

        Otherwise the same as in [`marshmallow.Schema`][marshmallow.Schema].

        Args:
            only:
                Whitelist of the declared fields to select when instantiating
                the Schema. If `None`, all fields are used. Nested fields can
                be represented with dot delimiters.
            exclude:
                Blacklist of the declared fields to exclude when instantiating
                the Schema. If a field appears in both `only` and `exclude`,
                it is not used. Nested fields can be represented with dot
                delimiters.
            context:
                Optional context passed to
                [`Method`][marshmallow.fields.Method] and
                [`Function`][marshmallow.fields.Function] fields.
            load_only:
                Fields to skip during serialization (write-only fields)
            dump_only:
                Fields to skip during deserialization (read-only fields)
            partial:
                Whether to ignore missing fields and not require any fields
                declared. Propagates down to
                [`Nested`][marshmallow.fields.Nested] fields as well. If its
                value is an iterable, only missing fields listed in that
                iterable will be ignored. Use dot delimiters to specify nested
                fields.
            unknown:
                Whether to exclude, include, or raise an error for unknown
                fields in the data. Use `EXCLUDE`, `INCLUDE` or `RAISE`.
            many:
                !!! warning
                    Changing this option schema-wide undermines the type
                    safety that this class aims to provide. Passing `True`
                    will therefore trigger a warning. You should instead use
                    the method-specific `many` parameter, when calling
                    [`dump`][marshmallow_generic.GenericSchema.dump]/
                    [`dumps`][marshmallow_generic.GenericSchema.dumps] or
                    [`load`][marshmallow_generic.GenericSchema.load]/
                    [`loads`][marshmallow_generic.GenericSchema.loads].
        """
        self._pre_init = True
        super().__init__(
            only=only,
            exclude=exclude,
            many=many,
            context=context,
            load_only=load_only,
            dump_only=dump_only,
            partial=partial,
            unknown=unknown,
        )
        self._pre_init = False

    def __setattr__(self, name: str, value: Any) -> None:
        """
        Warns, when trying to set `many` to anything other than `False`.

        Otherwise the same the normal
        [`object.__setattr__`](https://docs.python.org/3/reference/datamodel.html#object.__setattr__).
        """
        if name == "many" and value is not False:
            warn(MANY_SCHEMA_UNSAFE, stacklevel=4 if self._pre_init else 2)
        super().__setattr__(name, value)

    @post_load
    def instantiate(self, data: dict[str, Any], **_kwargs: Any) -> Model:
        """
        Unpacks `data` into the constructor of the specified **`Model`**.

        Registered as a
        [`@post_load`][marshmallow_generic.decorators.post_load]
        hook for the schema.

        !!! warning
            You should probably not use this method directly. No parsing,
            transformation or validation of any kind is done in this method.
            The `data` is passed to the **`Model`** constructor "as is".

        Args:
            data:
                The validated data after deserialization; will be unpacked
                into the constructor of the specified **`Model`** class.

        Returns:
            Instance of the schema's **`Model`** initialized with `**data`
        """
        return self._get_type_arg(0)(**data)

    if TYPE_CHECKING:

        @overload  # type: ignore[override]
        def dump(
            self,
            obj: Iterable[Model],
            *,
            many: Literal[True],
        ) -> list[dict[str, Any]]:
            ...

        @overload
        def dump(
            self,
            obj: Model,
            *,
            many: Optional[Literal[False]] = None,
        ) -> dict[str, Any]:
            ...

        def dump(
            self,
            obj: Union[Model, Iterable[Model]],
            *,
            many: Optional[bool] = None,
        ) -> Union[dict[str, Any], list[dict[str, Any]]]:
            """
            Serializes **`Model`** objects to native Python data types.

            Same as
            [`marshmallow.Schema.dump`][marshmallow.schema.Schema.dump]
            at runtime.

            Annotations ensure that type checkers will infer the return type
            correctly based on the `many` argument, and also enforce the `obj`
            argument to be an a `list` of **`Model`** instances, if `many` is
            set to `True` or a single instance of it, if `many` is `False`
            (or omitted).

            Args:
                obj:
                    The object or iterable of objects to serialize
                many:
                    Whether to serialize `obj` as a collection. If `None`, the
                    value for `self.many` is used.

            Returns:
                (dict[str, Any]): if `many` is set to `False`
                (list[dict[str, Any]]): if `many` is set to `True`
            """
            ...

        @overload  # type: ignore[override]
        def dumps(
            self,
            obj: Iterable[Model],
            *args: Any,
            many: Literal[True],
            **kwargs: Any,
        ) -> str:
            ...

        @overload
        def dumps(
            self,
            obj: Model,
            *args: Any,
            many: Optional[Literal[False]] = None,
            **kwargs: Any,
        ) -> str:
            ...

        def dumps(
            self,
            obj: Union[Model, Iterable[Model]],
            *args: Any,
            many: Optional[bool] = None,
            **kwargs: Any,
        ) -> str:
            """Same as [`dump`][marshmallow_generic.GenericSchema.dump], but returns a JSON-encoded string."""
            ...

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

            Same as
            [`marshmallow.Schema.load`][marshmallow.schema.Schema.load] at
            runtime, but data will always pass through the
            [`instantiate`][marshmallow_generic.schema.GenericSchema.instantiate]
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
                    fields declared. Propagates down to
                    [`Nested`][marshmallow.fields.Nested] fields as well. If
                    its value is an iterable, only missing fields listed in
                    that iterable will be ignored. Use dot delimiters to
                    specify nested fields.
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

            Same as
            [`marshmallow.Schema.loads`][marshmallow.schema.Schema.loads] at
            runtime, but data will always pass through the
            [`instantiate`][marshmallow_generic.schema.GenericSchema.instantiate]
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
                    fields declared. Propagates down to
                    [`Nested`][marshmallow.fields.Nested] fields as well. If
                    its value is an iterable, only missing fields listed in
                    that iterable will be ignored. Use dot delimiters to
                    specify nested fields.
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
