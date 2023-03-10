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
        self.assertIsNone(_util.GenericInsightMixin._type_arg)  # type: ignore[misc]

        # If the mixin type argument was not specified (still generic),
        # ensure that the attribute remains `None` on the subclass:
        t = TypeVar("t")

        class Foo:
            pass

        class Bar(Generic[t]):
            pass

        class TestSchema1(Bar[str], _util.GenericInsightMixin[t]):
            pass

        self.assertIsNone(TestSchema1._type_arg)  # type: ignore[misc]
        mock_super.assert_called_once()
        mock_super_meth.assert_called_once_with()

        mock_super.reset_mock()
        mock_super_meth.reset_mock()

        # If the mixin type argument was specified,
        # ensure it was assigned to the attribute on the child class:

        class TestSchema2(Bar[str], _util.GenericInsightMixin[Foo]):
            pass

        self.assertIs(Foo, TestSchema2._type_arg)  # type: ignore[misc]
        mock_super.assert_called_once()
        mock_super_meth.assert_called_once_with()

    def test__get_type_arg(self) -> None:
        with self.assertRaises(AttributeError):
            _util.GenericInsightMixin._get_type_arg()

        _type = object()
        with patch.object(_util.GenericInsightMixin, "_type_arg", new=_type):
            self.assertIs(_type, _util.GenericInsightMixin._get_type_arg())
