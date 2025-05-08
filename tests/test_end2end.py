from dataclasses import dataclass
from unittest import TestCase

from marshmallow import fields
from marshmallow_generic import GenericSchema

@dataclass
class Foo:
    field1: int
    field2: str

class FooSchema(GenericSchema[Foo]):
    field1 = fields.Integer()
    field2 = fields.String()

class TestEnd2End(TestCase):
    def test_end2end_dump(self) -> None:
        foo = Foo(field1=1, field2="test")
        schema = FooSchema()
        result = schema.dump(foo)

        self.assertEqual(result, {"field1": 1, "field2": "test"})

    def test_end2end_load(self) -> None:
        schema = FooSchema()
        result = schema.load({"field1": 1, "field2": "test"})

        self.assertEqual(result, Foo(field1=1, field2="test"))
