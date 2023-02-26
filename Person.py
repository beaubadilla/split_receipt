from collections import defaultdict
from typing import Dict, List

from Item import Item


class Person:
    count = 0

    def __init__(self, name):
        self._name: str = name
        self._total: float = 0.0
        self.purchases: Dict[str, List[Item]] = defaultdict(list)
        self.payment_preference: str = ...  # Venmo, Zelle, Splitwise(?)
        self.phone_number: str = ...
        self.email: str = ...

        self.id = Person.count
        self.increment_count()

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
        return round(self._total, 2)

    def add_individual_purchase(self, event, item):
        self.purchases[event].append(item)

    def add_shared_purchase(self, item, num_split_between: int):
        if event not in self.purchase:
            self.purchases[event] = []

        # if item.name
        price = round(item.price / num_split_between, 2)
        split_item = Item(item.name, price, item.tip, item.tax, 1)

    def get_event_total(self, event):
        return round(self.purchases[event]["total"], 2)

    def summary(self) -> str:
        ...
