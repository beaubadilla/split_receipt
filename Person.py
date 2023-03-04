from collections import defaultdict
from typing import Dict, List

from Item import Item


class Person:
    count = 0

    def __init__(self, name):
        self._name: str = name
        self._total: float = 0.0
        self.items: List[Item] = []
        # self.payment_preference: str = ...  # Venmo, Zelle, Splitwise(?)
        # self.phone_number: str = ...
        # self.email: str = ...

        # self.id = Person.count
        # self.increment_count()

    def __str__(self):
        return f"{self.name} ordered {self.purchases} totaling to {self.total}"

    @classmethod
    def increment_count(cls) -> None:
        cls.count += 1

    @classmethod
    def decrement_count(cls) -> None:
        cls.count -= 1

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def total(self):
        total = sum(item.base_price * item.count for item in self.items)

        tax = self.items[0].tax
        tip = self.items[0].tip
        total = total + (total * tax) + (total * tip)
        return total

    def add_individual_purchase(self, item):
        self.items.append(item)

    def add_shared_purchase(self, item, num_split_between: int):
        price = item.base_price / num_split_between
        split_item = Item(item.name, price, item.tip, item.tax, 1)
        self.items.append(split_item)

    def get_event_total(self, event):
        return round(self.purchases[event]["total"], 2)

    def summary(self) -> str:
        """
        (1)  LG Banana Coffee $  5.50
        (10) Coffee Bags      $165.00

        Subtotal              $170.50
        Tax (10.00%)          $ 17.05
        Tip (0.59%)           $  1.00

        Total                 $188.55

        Joseph H. and Peyton D.'s receipt for Spice-C
        ...
        """
        # Calculate first col length
        # consists of
        # parenthesis + number of digits of the largest count e.g. (1)
        # char limit for item name (arbitrary)
        max_count = max(item.count for item in self.items)
        num_digits_count = len(str(max_count))
        item_name_limit = 15
        num_delimiters = 2 + 1  # 2 parentheseses, 1 space
        first_col_length = num_digits_count + item_name_limit + num_delimiters

        subtotal = sum(item.base_price * item.count for item in self.items)

        # Use subtotal's number of digits because it might have more digits than any individual item
        # e.g.
        # item1 price=100, item2 price=5 -> num digits would equal 3
        # vs
        # item1 price=50, item2 price=50 -> num digits would equal 2 (when it should be 3) if we didn't use subtotal
        num_digits_price = len(str(subtotal))

        for item in self.items:
            count_str = f"({item.count:<{num_digits_count}})"
            item_name_str = f"{item.name:<{item_name_limit}.{item_name_limit}}"
            price_str = f"${item.base_price * item.count:<{num_digits_price}.2f}"

            print(f"{count_str} {item_name_str} {price_str}")

            tax = item.tax
            tip = item.tip

        # subtotal should inherently align
        tax_str = f"Tax: ({tax * 100:.2f}%)"
        tax_dollar = tax * subtotal

        tip_str = f"Tip: ({tip * 100:.2f}%)"
        tip_dollar = tip * subtotal

        total = subtotal + tax_dollar + tip_dollar

        print()
        print(f"{'Subtotal':<{first_col_length}} ${subtotal:.2f}")
        print(f"{tax_str:<{first_col_length}} ${tax_dollar:<{num_digits_price}.2f}")
        print(f"{tip_str:<{first_col_length}} ${tip_dollar:<{num_digits_price}.2f}")
        print()
        print(f"{'Total':<{first_col_length}} ${total:.2f}")
