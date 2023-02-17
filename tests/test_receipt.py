#!/usr/bin/python3
import unittest
from dataclasses import dataclass
from datetime import date

from Item import Item
from Event import Event
from Receipt import Receipt

class TestIdk(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()
    def tearDown(self) -> None:
        return super().tearDown()

    def test___str__(self):
        receipt = Receipt()
        receipt.event = Event("Phin Smith")
        receipt.items = {
            "Banana Coffee": Item(price=5.0, name="Banana Coffee")
        }
        receipt.items["Banana Coffee"].count = 1
        receipt.subtotal = 5.0
        receipt.tax = 0.095
        receipt.tip = 0
        receipt.paid_by = "Jake c"
        receipt.date = date.fromisoformat("2023-02-17")

        expect = (
            "Phin Smith"
            "Paid by Jake C on 2023-02-17"
            "(1) Banana Coffee\t$5.00"
            "Subtotal: $5.00"
            "Tax: 9.50%"
            "Tip: 0.00%"
            "Total: $5.47"
        )

        actual = receipt.__str__()
        self.assertEqual(expect, actual)


if __name__ == '__main__':
    unittest.main()
