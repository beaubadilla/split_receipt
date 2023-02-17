import unittest

import helpers


class TestHelpers(unittest.TestCase):
    def test_is_comma_delimited_true(self) -> None:
        test_cases: list[str] = [
            "Beau,Willie,Allen",
            "Beau, Willie,Allen",
            "Beau, Willie, Allen",
            "Beau, Willie, Allen ",
            " Beau, Willie, Allen ",
            "  Beau,  Willie, Allen  ",
            "Beau ,Willie  ,Allen  ",
            "  Beau  ,  Willie  ,  Allen  ",
        ]

        for tc in test_cases:
            with self.subTest(msg=tc):
                actual = helpers.is_comma_delimited(tc)
                self.assertTrue(actual)

    def test_is_comma_delimited_false(self) -> None:
        test_cases: list[str] = [
            "Beau Willie Allen",
            "Beau/Willie/Allen",
            "Beau+Willie+Allen",
            "Beau,Willie+Allen",
            "Beau,Willie Allen",
        ]

        for tc in test_cases:
            with self.subTest(msg=tc):
                actual = helpers.is_comma_delimited(tc)
                self.assertFalse(actual)

    def test_is_comma_delimited_exception(self) -> None:
        test_case = None

        self.assertRaises(ValueError, helpers.is_comma_delimited(test_case))


if __name__ == "__main__":
    unittest.main()
