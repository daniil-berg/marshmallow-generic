from unittest import TestCase
from unittest.mock import MagicMock, patch

from marshmallow_generic import _util, schema


class GenericSchemaTestCase(TestCase):
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
        mock__get_type_arg.assert_called_once_with()
        mock_cls.assert_called_once_with(**mock_data)

    def test_load(self) -> None:
        """Mainly for static type checking purposes."""

        class Foo:
            pass

        class TestSchema(schema.GenericSchema[Foo]):
            pass

        single: Foo = TestSchema().load({})
        self.assertIsInstance(single, Foo)

        multiple: list[Foo] = TestSchema().load([{}], many=True)
        self.assertIsInstance(multiple, list)
        self.assertIsInstance(multiple[0], Foo)
