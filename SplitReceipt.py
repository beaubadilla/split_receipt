from functools import wraps
import re
from typing import Dict, List, Set

from Person import Person
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
    """Repeat the prompt until there is valid input"""

    @wraps(func)
    def _required_input(*args):
        while not (response := func(*args)):
            continue
        return response

    return _required_input


input = required_input(input)


# input = required_input(input)


class SplitReceipt:
    def __init__(self) -> None:
        self.people = ...
        self.receipts = []
        self.items = ...

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
            # event_name = input(f"Event name? ")
            # subtotal = input(f"Subtotal? ")
            # tax = prompt_decimal("Tax? ")
            # tax = prompt_decimal("Tip? ")
        ...

    def prompt_orders(self):
        """Prompt for each item"""
        ...

    def summary(self):
        ...
