import unittest

import helpers


class TestHelpers(unittest.TestCase):
    def test_parse_names_one_name(self) -> None:
        names_str = "Jake"
        expect = ["Jake"]

        actual = helpers.parse_names(names_str)
        self.assertEqual(expect, actual)

    def test_parse_names_one_name_with_last_name(self) -> None:
        names_str = "Jake B"
        expect = ["Jake B"]

        actual = helpers.parse_names(names_str)
        self.assertEqual(expect, actual)

    def test_parse_names_two_names(self) -> None:
        names_str = "Jake and April"
        expect = ["Jake", "April"]

        actual = helpers.parse_names(names_str)
        self.assertEqual(expect, actual)

    def test_parse_names_two_names_with_last_name(self) -> None:
        names_str = "Jake B and April"
        expect = ["Jake B", "April"]

        actual = helpers.parse_names(names_str)
        self.assertEqual(expect, actual)

    def test_parse_names_multiple_names(self) -> None:
        names_str = "Jake, Alan K, and Wayne"
        expect = ["Jake", "Alan K", "Wayne"]

        actual = helpers.parse_names(names_str)
        self.assertEqual(expect, actual)

    def test_parse_names_multiple_names_with_last_name(self) -> None:
        names_str = "Jake, Alan K, and Wayne W W"
        expect = ["Jake", "Alan K", "Wayne W W"]

        actual = helpers.parse_names(names_str)
        self.assertEqual(expect, actual)

if __name__ == "__main__":
    unittest.main()
