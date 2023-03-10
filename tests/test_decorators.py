from collections.abc import Callable
from unittest import TestCase
from unittest.mock import MagicMock, patch

from marshmallow_generic import decorators


class DecoratorsTestCase(TestCase):
    @patch.object(decorators, "_post_load")
    def test_post_load(self, mock_original_post_load: MagicMock) -> None:
        mock_original_post_load.return_value = expected_output = object()

        def test_function(x: int) -> str:
            return str(x)

        pass_many, pass_original = MagicMock(), MagicMock()
        # Explicit annotation to possibly catch mypy errors:
        output: Callable[[int], str] = decorators.post_load(
            test_function,
            pass_many=pass_many,
            pass_original=pass_original,
        )
        self.assertIs(expected_output, output)
        mock_original_post_load.assert_called_once_with(
            test_function,
            pass_many=pass_many,
            pass_original=pass_original,
        )
