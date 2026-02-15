__copyright__ = "© 2023 Daniel Fainberg"
__license__ = """Apache-2.0

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License."""

__version__ = "4.0.0"

__doc__ = """
Generic schema with full typing support and minimal boilerplate.
"""

# Most of these are re-exported from marshmallow.
__all__ = [
    "EXCLUDE",
    "INCLUDE",
    "RAISE",
    "GenericSchema",  # custom
    "Schema",
    "SchemaOpts",
    "ValidationError",
    "fields",
    "missing",
    "post_dump",
    "post_load",  # custom
    "pre_dump",
    "pre_load",
    "validates",
    "validates_schema",
]

from marshmallow import fields
from marshmallow.constants import EXCLUDE, INCLUDE, RAISE, missing
from marshmallow.decorators import (  # `post_load` overloaded
    post_dump,
    pre_dump,
    pre_load,
    validates,
    validates_schema,
)
from marshmallow.exceptions import ValidationError
from marshmallow.schema import Schema, SchemaOpts

from marshmallow_generic.decorators import post_load
from marshmallow_generic.schema import GenericSchema
