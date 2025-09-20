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

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """
        Ensure KeyError is raised when the key path does not exist.
        Also verify the KeyError message matches the missing key.
        """
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        # KeyError message is "'missing_key'"
        self.assertEqual(str(cm.exception), f"'{path[-1]}'")


if __name__ == "__main__":
    unittest.main()
