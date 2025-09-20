#!/usr/bin/env python3
"""
Unit tests for utils.access_nested_map using parameterized inputs.
"""

import unittest
from parameterized import parameterized
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """Tests for the access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Ensure access_nested_map returns the correct value for given path."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    def test_access_nested_map_exception(self, nested_map, path):
            """
            Ensure KeyError is raised when the key path does not exist.
            Also verify the KeyError message matches the missing key.
            """
            with self.assertRaises(KeyError) as cm:
                access_nested_map(nested_map, path)
            # The KeyError message is usually the missing key, e.g., "'a'"
            self.assertEqual(str(cm.exception), repr(path[len(cm.exception.args[0]) - 1] if isinstance(cm.exception.args[0], tuple) else cm.exception.args[0]))
            # Simpler and correct for this function:
            self.assertEqual(str(cm.exception), f"'{path[len(cm.exception.args[0])-1]}'")


if __name__ == "__main__":
    unittest.main()
