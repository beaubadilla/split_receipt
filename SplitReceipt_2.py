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

    def prompt_event_name(self) -> str:
        event_name: str = input(f"Event? ")

        if event_name.upper() == event_name:
            return event_name
        else:
            return event_name.title()

    def prompt_receipt_details() -> Receipt:
        receipt = Receipt()
        receipt.prompt_details()

        return receipt

    def prompt_people(self) -> List[str]:
        names: str = input(f"List of people: ")
        names: List[str] = names.split(",")
        names: List[str] = [person.title() for person in names]

        return names

    def run(self) -> None:
        event_name = self.prompt_event_name()

        names = self.prompt_people()
        squad = Squad()
        for name in names:
            squad.add(Person(name))

        receipt: Receipt = self.prompt_receipt_details()  # TODO: refactor

        orders: List[str] = self.prompt_orders()
        orders_info: List[Set[str, str, str]] = self.parse_orders()

        for names, kw, item_names in orders_info:
            for name in names:
                person = squad.get(name)
                for item_name in item_names:
                    item = receipt.get(item_name)

                    if kw == "got":
                        person.add_individual_purchase(item)
                    elif kw == "shared":
                        num_splits = len(names)
                        person.add_shared_purchase(item, num_splits)

        for name, person in squad.people:
            print(person.summary())


if __name__ == "__main__":
    SplitReceipt().run()
