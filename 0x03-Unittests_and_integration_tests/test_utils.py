# #!/usr/bin/env python3
# """
# Unit tests for utils.access_nested_map using parameterized inputs.
# """

# import unittest
# from parameterized import parameterized
# from utils import access_nested_map


# class TestAccessNestedMap(unittest.TestCase):
#     """Tests for the access_nested_map function."""

#     @parameterized.expand([
#         ({"a": 1}, ("a",), 1),
#         ({"a": {"b": 2}}, ("a",), {"b": 2}),
#         ({"a": {"b": 2}}, ("a", "b"), 2),
#     ])
#     def test_access_nested_map(self, nested_map, path, expected):
#         """Ensure access_nested_map returns the correct value for given path."""
#         self.assertEqual(access_nested_map(nested_map, path), expected)

#     @parameterized.expand([
#         ({}, ("a",)),
#         ({"a": 1}, ("a", "b")),
#     ])
#     def test_access_nested_map_exception(self, nested_map, path):
#         """
#         Ensure KeyError is raised when the key path does not exist.
#         Also verify the KeyError message matches the missing key.
#         """
#         with self.assertRaises(KeyError) as cm:
#             access_nested_map(nested_map, path)
#         # KeyError message is "'missing_key'"
#         self.assertEqual(str(cm.exception), f"'{path[-1]}'")


# if __name__ == "__main__":
#     unittest.main()


#!/usr/bin/env python3
"""
Unit tests for utils module.
"""

import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json


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
        """Ensure KeyError is raised and message matches the missing key."""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), f"'{path[-1]}'")


class TestGetJson(unittest.TestCase):
    """Tests for the get_json function."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        """
        Test that utils.get_json returns the expected payload and
        that requests.get is called exactly once with the correct URL.
        """
        # Patch 'requests.get' inside the utils module
        with patch("utils.requests.get") as mock_get:
            mock_resp = Mock()
            mock_resp.json.return_value = test_payload
            mock_get.return_value = mock_resp

            result = get_json(test_url)

            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)


if __name__ == "__main__":
    unittest.main()
