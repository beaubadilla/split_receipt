from datetime import datetime, date
import re
from typing import Dict, List

from Item import Item
from Event import Event

# Matches "100%", "0%", "99%", "51%", "51.5%", "18%", "18.213%", "0.5%", "1%"
PERCENTAGE_REGEX = re.compile(r"^[0-9]+\.?[0-9]+%$")

DECIMAL_REGEX = re.compile(r"^[0-9]+\.[0-9]+$")
DOLLAR_REGEX = re.compile(r"^\$[0-9]+\.?[0-9]*$")


class Receipt:
    def __init__(self) -> None:
        self.event: Event = ...
        self.subtotal: float = ...
        self._total: float = ...
        self.tip: float = ...
        self.tax: float = ...
        self.date: date = ...
        self.items: Dict[str, Item] = {}
        self.paid_by: str = ...
        self.discount: float = ...

    def prompt_details(self):
        self.event = self.prompt_event()
        self.subtotal = self.prompt_subtotal()
        self.tax = self.prompt_tax()
        self.tip = self.prompt_tip()
        self.date = self.prompt_date()
        self.items = self.prompt_items()
        self.paid_by = self.prompt_paid_by()
        # self.discount = self.prompt_discount()

    def prompt_event(self) -> str:
        self.event = Event(input("Event Name"))
        return self.event

    def prompt_subtotal(self) -> float:
        while not (DOLLAR_REGEX.match(response := input("Subtotal? "))):
            print('Invalid input. Example: "$30.13"')

        _, subtotal = response.split("$")
        subtotal = float(subtotal)

        self.subtotal = subtotal
        return self.subtotal

    @property
    def total(self) -> float:
        return self.subtotal + (self.tax * self.subtotal) + (self.tip * self.subtotal)

    def prompt_tip(self) -> float:
        accepted: bool = False
        tip: float = None
        while not accepted:
            response: str = input("Tip? ")
            if DECIMAL_REGEX.match(response):
                tip = float(response)
                accepted = True
            elif PERCENTAGE_REGEX.match(response):
                tip, _ = response.split("%")
                tip = float(tip)
                accepted = True
            elif DOLLAR_REGEX.match(response):
                # separate from dollar sign
                _, tip = response.split("$")
                tip = float(tip)
                accepted = True
            else:
                print(f"Invalid input. Acceptable formats: 18%, 18.0%, 0.18")

        self.tip = tip
        return self.tip

    def prompt_tax(self) -> float:
        accepted: bool = False
        tax: float = None
        while not accepted:
            response: str = input("Tax? ")
            if DECIMAL_REGEX.match(response):
                tax = float(response)
                accepted = True
            elif PERCENTAGE_REGEX.match(response):
                tax, _ = response.split("%")
                tax = float(tax)
                accepted = True
            elif DOLLAR_REGEX.match(response):
                # separate from dollar sign
                _, tax = response.split("$")
                tax = float(tax)
                accepted = True
            else:
                print(f"Invalid input. Acceptable formats: 18%, 18.0%, 0.18")

        self.tax = tax
        return self.tax

    def prompt_date(self) -> date:
        accepted: bool = False
        while not accepted:
            response = input(f"When did this event happen (YYYY-MM-DD)? ")
            try:
                date_ = date.fromisoformat(response)
            except ValueError as ve:
                print("Invalid input. Acceptable formats: 1996-01-16")
            else:
                accepted = True

        self.date = date_
        return self.date

    def prompt_items(self) -> Dict[str, Item]:
        print('Enter "DONE" when there are no more items.')
        while (name := input("Name of item? ")) != "done":
            # All upper means it is an acronym. Leave as is
            if name.upper() != name:
                name = name.title()

            price = input(f"Price of {name}? ")
            count = input(f'How many "{name}"? ')
            if name in self.items:
                print(f"{name} already exists. Adding {count} more.")
                self.items[name].count += count
                print(f"Total {name} = {self.items[name].count}")
            else:
                item = Item(name, price, count)
                self.items[name.lower()] = item

        return self.items

    def prompt_paid_by(self) -> str:
        paid_by = input("Who paid? ").title()
        self.paid_by = paid_by
        return self.paid_by
