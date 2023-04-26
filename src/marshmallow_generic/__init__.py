__copyright__ = "© 2023 Daniil Fajnberg"
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

__version__ = "1.0.1"

__doc__ = """
Generic schema with full typing support and minimal boilerplate.
"""

__all__ = [
    # Custom:
    "GenericSchema",
    "post_load",
    # Re-exports from marshmallow:
    "EXCLUDE",
    "INCLUDE",
    "RAISE",
    "Schema",
    "SchemaOpts",
    "fields",
    "validates",
    "validates_schema",
    "pre_dump",
    "post_dump",
    "pre_load",
    # "post_load",
    "pprint",
    "ValidationError",
    "missing",
]

from marshmallow import fields
from marshmallow.decorators import (  # `post_load` overloaded
    post_dump,
    pre_dump,
    pre_load,
    validates,
    validates_schema,
)
from marshmallow.exceptions import ValidationError
from marshmallow.schema import Schema, SchemaOpts
from marshmallow.utils import EXCLUDE, INCLUDE, RAISE, missing, pprint

from marshmallow_generic.decorators import post_load
from marshmallow_generic.schema import GenericSchema
