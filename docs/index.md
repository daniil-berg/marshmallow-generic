# marshmallow-generic

**Generic schema with full typing support and minimal boilerplate**

---

**Documentation**: <a href="http://daniil-berg.github.io/marshmallow-generic" target="_blank"> daniil-berg.github.io/marshmallow-generic </a>

**Source Code**: <a href="https://github.com/daniil-berg/marshmallow-generic" target="_blank"> github.com/daniil-berg/marshmallow-generic </a>

---

Extension for <a href="https://github.com/marshmallow-code/marshmallow" target="_blank">**`marshmallow`**</a> to make <a href="https://marshmallow.readthedocs.io/en/stable/quickstart.html#deserializing-to-objects" target="_blank">deserialization to objects</a> easier and improve type safety.

The main `GenericSchema` class extends <a href="https://marshmallow.readthedocs.io/en/stable/marshmallow.schema.html#marshmallow.schema.Schema" target="_blank">`marshmallow.Schema`</a> making it **generic** in terms of the class that data should be deserialized to, when calling <a href="https://marshmallow.readthedocs.io/en/stable/marshmallow.schema.html#marshmallow.schema.Schema.load" target="_blank">`load`/`loads`</a>.

With `GenericSchema` there is no need to explicitly write `post_load` hooks to initialize the object anymore. 🎉

If the "model" class is (for example) `User`, it just needs to be passed as the type argument, when subclassing `GenericSchema`. The output of the `load`/`loads` method will then be automatically inferred as either `User` or `list[User]` (depending on whether `many` is `True` or not) by any competent type checker. ✨

## Usage Example

```python
from marshmallow_generic import GenericSchema, fields


class User:
    def __init__(self, name: str, email: str) -> None:
        self.name = name
        self.email = email

    def __repr__(self) -> str:
        return "<User(name={self.name!r})>".format(self=self)

...

class UserSchema(GenericSchema[User]):
    name = fields.Str()
    email = fields.Email()


user_data = {"name": "Monty", "email": "monty@python.org"}
schema = UserSchema()
single_user = schema.load(user_data)
print(single_user)  # <User(name='Monty')>

json_data = '''[
    {"name": "Monty", "email": "monty@python.org"},
    {"name": "Ronnie", "email": "ronnie@stones.com"}
]'''
multiple_users = schema.loads(json_data, many=True)
print(multiple_users)  # [<User(name='Monty')>, <User(name='Ronnie')>]
```

Adding `reveal_type(single_user)` and `reveal_type(multiple_users)` at the bottom and running that code through <a href="https://mypy.readthedocs.io/en/stable/" target="_blank">`mypy`</a> would yield the following output:

```
# note: Revealed type is "User"
# note: Revealed type is "builtins.list[User]"
```

With the regular `marshmallow.Schema`, the output of `mypy` would instead be this:

```
# note: Revealed type is "Any"
# note: Revealed type is "Any"
```

This also means your IDE will be able to infer the types and thus provide useful auto-suggestions for the loaded objects. 👨‍💻

Here is PyCharm with the example from above:

![Image title](http://daniil-berg.github.io/marshmallow-generic/img/ide_suggestion_user.png)

## Installation

`pip install marshmallow-generic`

## Dependencies

Python Version `3.9+` and `marshmallow` (duh)
