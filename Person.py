from Item import Item


class Person:
    count = 0

    def __init__(self, name):
        self._name: str = name
        self._total: float = 0.0
        self.purchases: list[Item] = []
        self.payment_preference: str = ...  # Venmo, Zelle, Splitwise(?)
        self.phone_number: str = ...
        self.email: str = ...

        self.id = Person.count

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

    def add_purchase(self, event, item, price, tax, tip):
        # TODO: refactor. seems redundant to always pass tax/tip
        if event not in self.purchases:
            self.purchases[event] = {}
            self.purchases[event]["tax"] = tax
            self.purchases[event]["tip"] = tip
            self.purchases[event]["orders"] = {}
            self.purchases[event]["total"] = 0
        self.purchases[event]["orders"][item] = price

        purchase_total = price + (price * tax) + (price * tip)
        self.purchases[event]["total"] += purchase_total
        self._total += purchase_total

    def get_event_total(self, event):
        return round(self.purchases[event]["total"], 2)
