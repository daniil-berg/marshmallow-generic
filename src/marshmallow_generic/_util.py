from typing import (
    Any,
    Generic,
    Literal,
    Optional,
    TypeVar,
    Union,
    get_args,
    get_origin,
    overload,
)

_T0 = TypeVar("_T0")
_T1 = TypeVar("_T1")
_T2 = TypeVar("_T2")
_T3 = TypeVar("_T3")
_T4 = TypeVar("_T4")


class GenericInsightMixin(Generic[_T0, _T1, _T2, _T3, _T4]):
    _type_arg_0: Optional[type[_T0]] = None
    _type_arg_1: Optional[type[_T1]] = None
    _type_arg_2: Optional[type[_T2]] = None
    _type_arg_3: Optional[type[_T3]] = None
    _type_arg_4: Optional[type[_T4]] = None

    @classmethod
    def __init_subclass__(cls, **kwargs: Any) -> None:
        """Saves the type argument in the `_type_arg` class attribute."""
        super().__init_subclass__(**kwargs)
        for base in cls.__orig_bases__:  # type: ignore[attr-defined]
            origin = get_origin(base)
            if origin is None or not issubclass(origin, GenericInsightMixin):
                continue
            type_args = get_args(base)
            for idx, arg in enumerate(type_args):
                # Do not set the attribute for generics:
                if isinstance(arg, TypeVar):
                    continue
                # Do not set `NoneType`:
                if isinstance(arg, type) and isinstance(None, arg):
                    continue
                setattr(cls, f"_type_arg_{idx}", arg)
            return

    @classmethod
    @overload
    def _get_type_arg(cls, idx: Literal[0]) -> type[_T0]:
        ...

    @classmethod
    @overload
    def _get_type_arg(cls, idx: Literal[1]) -> type[_T1]:
        ...

    @classmethod
    @overload
    def _get_type_arg(cls, idx: Literal[2]) -> type[_T2]:
        ...

    @classmethod
    @overload
    def _get_type_arg(cls, idx: Literal[3]) -> type[_T3]:
        ...

    @classmethod
    @overload
    def _get_type_arg(cls, idx: Literal[4]) -> type[_T4]:
        ...

    @classmethod
    def _get_type_arg(
        cls,
        idx: Literal[0, 1, 2, 3, 4],
    ) -> Union[type[_T0], type[_T1], type[_T2], type[_T3], type[_T4]]:
        """Returns the type argument of the class (if specified)."""
        if idx == 0:
            type_ = cls._type_arg_0
        elif idx == 1:
            type_ = cls._type_arg_1
        elif idx == 2:  # noqa: PLR2004
            type_ = cls._type_arg_2
        elif idx == 3:  # noqa: PLR2004
            type_ = cls._type_arg_3
        elif idx == 4:  # noqa: PLR2004
            type_ = cls._type_arg_4
        else:
            raise ValueError("Only 5 type parameters available")
        if type_ is None:
            raise AttributeError(
                f"{cls.__name__} is generic; type argument {idx} unspecified"
            )
        return type_


class GenericInsightMixin1(GenericInsightMixin[_T0, None, None, None, None]):
    pass


class GenericInsightMixin2(GenericInsightMixin[_T0, _T1, None, None, None]):
    pass
