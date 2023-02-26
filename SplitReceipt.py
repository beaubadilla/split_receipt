from functools import wraps
import re
from typing import Dict, List, Set

import helpers
from Person import Person
from Squad import Squad
from Receipt import Receipt

# Matches "100%", "0%", "99%", "51%", "51.5%", "18%", "18.213%", "0.5%", "1%"
PERCENTAGE_REGEX = re.compile(r"^[0-9]+\.?[0-9]+%$")

DECIMAL_REGEX = re.compile(r"^[0-9]+\.[0-9]+$")
DOLLAR_REGEX = re.compile(r"^\$[0-9]+\.?[0-9]*$")

# def comma_delimiter(func):
#     @wraps(func)
#     def _comma_delimiter(*args):
#         result = func(*args)

#         if ''
#         stack_of_inputs.append(result)
#         return result

#     return _comma_delimiter

# def required_input(prompt: str) -> str:
#     """Repeat the prompt until there is valid input"""
#     while not (response := input("test prompt")):
#         continue
#     return response


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
        self.people = ...
        self.receipts = []
        self.items = ...
        self.orders: List[str] = []

    def prompt_people(self) -> List[str]:
        people: str = input(f"List of people: ")
        people: List[str] = people.split(",")
        people: List[str] = [person.title() for person in people]

        self.people = [Person(person) for person in people]

        return self.people

    def prompt_receipt_details(self):
        # What is the subtotal
        # What is the tax, either in % or the value
        # What is the tip, either in % or the value
        # List each item
        #   name
        #   price
        num_receipts: int = int(input(f"How many receipts? "))

        for _ in range(num_receipts):
            receipt = Receipt()
            receipt.prompt_details()
            self.receipts.append(receipt)
            print(receipt)

        return self.receipts

    def prompt_orders(self):
        """Prompt for each item"""
        orders = []
        print("Who got what?")
        print('Enter "DONE" when finished')
        while (response := input("> ")) != "DONE":
            response_split = response.split()

            required_keywords = {"got", "shared", "covered"}
            if not any(kw in response_split for kw in required_keywords):
                print(f"Did not find any keywords ({', '.join(required_keywords)})")

            orders.append(response)

        self.orders = orders
        return self.orders

    def parse_orders(self):
        parsed = []
        for order in self.orders:
            if "got" in order.split():
                kw = "got"
            elif "shared" in order.split():
                kw = "shared"
            elif "covered" in order.split():
                kw = "covered"
            names, items = order.split(kw)

            names: List[str] = helpers.parse_names(names)
            items = helpers.parse_names(items)
            parsed.append((names, kw, items))

        return parsed

    def add_individual_purchase(self, names, items):
        people = [self.people[name] for name in names]

    def summary(self):
        ...

    def run(self):
        squad = Squad()

        # Get all involved people
        people: List[Person] = self.prompt_people()
        for person in people:
            squad.add(person)

        # Get details of all receipts
        ## Create events
        ## Create items
        receipts: List[Receipt] = self.prompt_receipt_details()
        item_name_to_event = {
            item.name: receipt.event.name
            for receipt in receipts
            for item in receipt.items.values()
        }
        events = [receipt.event.name for receipt in receipts]
        print(f"{item_name_to_event=}")
        print(f"{events=}")

        # Get all purchases
        # purchases: List[Purchase] = self.prompt_orders()
        purchases: List[str] = self.prompt_orders()
        purchases_info: List[Set[str, str, str]] = self.parse_orders()
        print(f"{purchases=}")
        print(f"{purchases_info=}")

        # For each order,
        # using details from Receipts
        # populate each person's info
        for names, kw, item_names in purchases_info:
            for name in names:
                person = squad.get(name)
                for item_name in item_names:
                    event_name = item_name_to_event[item_name]
                    
                    for receipt in receipts:
                        if receipt.has(item_name):
                            

                    if kw == "got":
                        person.add_individual_purchase(event_name, item)
            ...
            # for each name
            #     for each item
            #         if kw == "got":
            #             add individual purchase
            #         elif kw == "shared":
            #             num_splits = len(names)
            #             add split purchase(item, num_splits)

        # For each person,
        # retrieve summary
        ## for each event, print personal "receipt"
        for name, person in squad.squad.items():
            print(person.summary())


if __name__ == "__main__":
    app = SplitReceipt()
    app.run()
