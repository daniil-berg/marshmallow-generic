from typing import Any
from unittest import TestCase
from unittest.mock import MagicMock, patch

from marshmallow_generic import _util, schema


class GenericSchemaTestCase(TestCase):
    @patch("marshmallow.schema.Schema.__init__")
    def test___init__(self, mock_super_init: MagicMock) -> None:
        class Foo:
            pass

        kwargs: dict[str, Any] = {
            "only": object(),
            "exclude": object(),
            "context": object(),
            "load_only": object(),
            "dump_only": object(),
            "partial": object(),
            "unknown": object(),
            "many": object(),
        }
        schema.GenericSchema[Foo](**kwargs)
        mock_super_init.assert_called_once_with(**kwargs)

    def test___setattr__(self) -> None:
        class Foo:
            pass

        obj = schema.GenericSchema[Foo]()
        with self.assertWarns(UserWarning):
            obj.many = new = MagicMock()
        self.assertIs(new, obj.many)

    @patch.object(_util.GenericInsightMixin, "_get_type_arg")
    def test_instantiate(self, mock__get_type_arg: MagicMock) -> None:
        mock__get_type_arg.return_value = mock_cls = MagicMock()
        mock_data = {"foo": "bar", "spam": 123}

        class Foo:
            pass

        schema_obj = schema.GenericSchema[Foo]()
        # Explicit annotation to possibly catch mypy errors:
        output: Foo = schema_obj.instantiate(mock_data)
        self.assertIs(mock_cls.return_value, output)
        mock__get_type_arg.assert_called_once_with(0)
        mock_cls.assert_called_once_with(**mock_data)

    def test_dump_and_dumps(self) -> None:
        """Mainly for static type checking purposes."""

        class Foo:
            pass

        class TestSchema(schema.GenericSchema[Foo]):
            pass

        foo = Foo()
        single: dict[str, Any] = TestSchema().dump(foo)
        self.assertDictEqual({}, single)
        json_string: str = TestSchema().dumps(foo)
        self.assertEqual("{}", json_string)

        multiple: list[dict[str, Any]] = TestSchema().dump([foo], many=True)
        self.assertListEqual([{}], multiple)
        json_string = TestSchema().dumps([foo], many=True)
        self.assertEqual("[{}]", json_string)

    def test_load_and_loads(self) -> None:
        """Mainly for static type checking purposes."""

        class Foo:
            pass

        class TestSchema(schema.GenericSchema[Foo]):
            pass

        single: Foo
        single = TestSchema().load({})
        self.assertIsInstance(single, Foo)
        single = TestSchema().loads("{}")
        self.assertIsInstance(single, Foo)

        multiple: list[Foo]
        multiple = TestSchema().load([{}], many=True)
        self.assertIsInstance(multiple, list)
        self.assertIsInstance(multiple[0], Foo)
        multiple = TestSchema().loads("[{}]", many=True)
        self.assertIsInstance(multiple, list)
        self.assertIsInstance(multiple[0], Foo)
