from typing import Generic, TypeVar
from unittest import TestCase
from unittest.mock import MagicMock, patch

from marshmallow_generic import _util


class GenericInsightMixinTestCase(TestCase):
    @patch.object(_util, "super")
    def test___init_subclass__(self, mock_super: MagicMock) -> None:
        mock_super_meth = MagicMock()
        mock_super.return_value = MagicMock(__init_subclass__=mock_super_meth)

        # Should be `None` by default:
        self.assertIsNone(_util.GenericInsightMixin._type_arg_0)  # type: ignore[misc]
        self.assertIsNone(_util.GenericInsightMixin._type_arg_1)  # type: ignore[misc]
        self.assertIsNone(_util.GenericInsightMixin._type_arg_2)  # type: ignore[misc]
        self.assertIsNone(_util.GenericInsightMixin._type_arg_3)  # type: ignore[misc]
        self.assertIsNone(_util.GenericInsightMixin._type_arg_4)  # type: ignore[misc]

        # If the mixin type argument was not specified (still generic),
        # ensure that the attribute remains `None` on the subclass:
        t = TypeVar("t")

        class Foo:
            pass

        class Bar(Generic[t]):
            pass

        class TestCls(Bar[str], _util.GenericInsightMixin[t, None, int, str, bool]):
            pass

        self.assertIsNone(TestCls._type_arg_0)  # type: ignore[misc]
        self.assertIsNone(TestCls._type_arg_1)  # type: ignore[misc]
        self.assertIs(int, TestCls._type_arg_2)  # type: ignore[misc]
        self.assertIs(str, TestCls._type_arg_3)  # type: ignore[misc]
        self.assertIs(bool, TestCls._type_arg_4)  # type: ignore[misc]
        mock_super.assert_called_once()
        mock_super_meth.assert_called_once_with()

        mock_super.reset_mock()
        mock_super_meth.reset_mock()

        # If the mixin type arguments were omitted,
        # ensure the attributes remained `None`:

        class UnspecifiedCls(_util.GenericInsightMixin):  # type: ignore[type-arg]
            pass

        self.assertIsNone(UnspecifiedCls._type_arg_0)  # type: ignore[misc]
        self.assertIsNone(UnspecifiedCls._type_arg_1)  # type: ignore[misc]
        self.assertIsNone(UnspecifiedCls._type_arg_2)  # type: ignore[misc]
        self.assertIsNone(UnspecifiedCls._type_arg_3)  # type: ignore[misc]
        self.assertIsNone(UnspecifiedCls._type_arg_4)  # type: ignore[misc]
        mock_super.assert_called_once()
        mock_super_meth.assert_called_once_with()

    def test__get_type_arg(self) -> None:
        with self.assertRaises(AttributeError):
            _util.GenericInsightMixin._get_type_arg(0)

        _type_0 = object()
        _type_1 = object()
        _type_2 = object()
        _type_3 = object()
        _type_4 = object()
        with patch.multiple(
            _util.GenericInsightMixin,
            _type_arg_0=_type_0,
            _type_arg_1=_type_1,
            _type_arg_2=_type_2,
            _type_arg_3=_type_3,
            _type_arg_4=_type_4,
        ):
            self.assertIs(_type_0, _util.GenericInsightMixin._get_type_arg(0))
            self.assertIs(_type_1, _util.GenericInsightMixin._get_type_arg(1))
            self.assertIs(_type_2, _util.GenericInsightMixin._get_type_arg(2))
            self.assertIs(_type_3, _util.GenericInsightMixin._get_type_arg(3))
            self.assertIs(_type_4, _util.GenericInsightMixin._get_type_arg(4))
            with self.assertRaises(ValueError):
                _util.GenericInsightMixin._get_type_arg(5)  # type: ignore[call-overload]
