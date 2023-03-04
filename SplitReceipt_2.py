from functools import wraps
import re
from typing import Dict, List, Set

import helpers
from Person import Person
from Squad import Squad
from Receipt import Receipt


def required_input(func):
    """Repeat the prompt until there is some input"""

    @wraps(func)
    def _required_input(*args):
        while not (response := func(*args)):
            continue
        return response

    return _required_input


input = required_input(input)


class SplitReceipt:
    def __init__(self) -> None:
        self.squad = Squad()
        self.receipt = Receipt()

    def prompt_people(self) -> List[str]:
        names: str = input(f"List of people: ")
        names: List[str] = names.split(",")
        names: List[str] = [person.title() for person in names]

        return names

    def prompt_receipt_details(self) -> Receipt:
        self.receipt.prompt_details()

        return self.receipt

    def prompt_orders(self) -> List[str]:
        orders = []
        print("Who got what?")
        print('Enter "DONE" when finished')
        while (response := input("> ")) != "DONE":
            if not self.valid_order(response):
                continue

            orders.append(response)

        return orders

    def valid_order(self, order: str):
        required_keywords = {"got", "shared", "covered"}
        try:
            names, _, item_names = self.parse_order(order)
        except NameError:
            print(f"Did not find any keywords ({', '.join(required_keywords)})")
        except Exception:
            print(f"Invalid order format e.g. Jake got fries")

        # Check for valid name
        for name in names:
            if name not in self.squad.names:
                print(f"{name} not found.")
                return False

        # Check for valid item names
        for item_name in item_names:
            if item_name not in self.receipt.item_names:
                print(f"{item_name} not found.")
                return False

        return True

    def parse_order(self, order: str) -> Set:
        if "got" in order.split():
            kw = "got"
        elif "shared" in order.split():
            kw = "shared"
        elif "covered" in order.split():
            kw = "covered"
        names, item_names = order.split(kw)

        names: List[str] = helpers.parse_names(names)
        item_names = helpers.parse_names(item_names)

        return names, kw, item_names

    def run(self) -> None:
        # self.prompt_event_name()

        names = self.prompt_people()
        for name in names:
            self.squad.add(Person(name))

        receipt: Receipt = self.prompt_receipt_details()

        self.event_name = receipt.event.name

        orders: List[str] = self.prompt_orders()
        orders_info: List[Set[str, str, str]] = [
            self.parse_order(order) for order in orders
        ]

        for names, kw, item_names in orders_info:
            for name in names:
                person = self.squad.get(name)
                for item_name in item_names:
                    item = receipt.get(item_name)

                    if kw == "got":
                        person.add_individual_purchase(item)
                    elif kw == "shared":
                        num_splits = len(names)
                        person.add_shared_purchase(item, num_splits)

        for name, person in self.squad.people.items():
            print(f"\n{name.title()}'s receipt for {self.event_name}")

            print(person.summary())

        people = self.squad.people.values()
        total = sum(person.total for person in people)
        print()
        print(f"Receipt total=${receipt.total:.2f}. Orders total=${total:.2f}")


if __name__ == "__main__":
    SplitReceipt().run()
