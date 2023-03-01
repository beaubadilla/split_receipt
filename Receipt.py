from datetime import datetime, date
import re
from typing import Dict, List

import helpers
from Item import Item
from Event import Event

# Matches "100%", "0%", "99%", "51%", "51.5%", "18%", "18.213%", "0.5%", "1%"
PERCENTAGE_REGEX = re.compile(r"^[0-9]+\.?[0-9]+%$")

DECIMAL_REGEX = re.compile(r"^[0-9]+\.[0-9]+$")
DOLLAR_REGEX = re.compile(r"^\$[0-9]+\.?[0-9]*$")


class Receipt:
    def __init__(
        self,
        event: Event = None,
        subtotal: float = None,
        total: float = None,
        tip: float = None,
        tax: float = None,
        date_: date = None,
        paid_by: str = None,
    ) -> None:
        self.event: Event = event
        self.subtotal: float = subtotal
        self._total: float = total
        self.tip: float = tip
        self.tax: float = tax
        self.date: date = date_
        self.items: Dict[str, Item] = {}
        self.paid_by: str = paid_by
        self.discount: float = None

    @property
    def item_names(self):
        return self.items.keys()

    def __str__(self) -> None:
        if not self.event:
            return "No receipt details"

        items_str = "\n".join(
            [
                f"({item.count}) {item.name}\t${item.price:.2f}"
                for item in self.items.values()
            ]
        )
        str_ = (
            f"{self.event.name}"
            f"Paid by {self.paid_by.title()} on {self.date}"
            f"{items_str}"
            f"Subtotal: ${self.subtotal:0.2f}"
            f"Tax: {self.tax * 100:0.2f}%"
            f"Tip: {self.tip * 100:0.2f}%"
            f"Total: ${self.total:0.2f}"
        )
        return str_

    def prompt_details(self):
        self.prompt_event()
        self.prompt_subtotal()
        self.prompt_tax()
        self.prompt_tip()
        self.prompt_date()
        self.prompt_items()
        self.prompt_paid_by()
        # self.discount = self.prompt_discount()

    def prompt_event(self) -> str:
        self.event = Event(input("Event Name? "))
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
            if DECIMAL_REGEX.match(response) or response == "0":
                tip = float(response)
                accepted = True
            elif PERCENTAGE_REGEX.match(response):
                tip, _ = response.split("%")
                tip = float(tip) / 100
                accepted = True
            elif DOLLAR_REGEX.match(response):
                # separate from dollar sign
                _, tip = response.split("$")
                tip = float(tip)
                tip = tip / self.subtotal
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
            if DECIMAL_REGEX.match(response) or response == "0":
                tax = float(response)
                accepted = True
            elif PERCENTAGE_REGEX.match(response):
                tax, _ = response.split("%")
                tax = float(tax) / 100
                accepted = True
            elif DOLLAR_REGEX.match(response):
                _, tax = response.split("$")
                tax = float(tax)
                tax = tax / self.subtotal
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
        while (name := input("Name of item? ")) != "DONE":
            # All upper means it is an acronym. Leave as is
            if name.upper() != name:
                name = name.title()

            base_price = self.prompt_base_price(name)
            count = int(input(f'How many "{name}"? '))
            if name in self.items:
                print(f"{name} already exists. Adding {count} more.")
                self.items[name].count += count
                print(f"Total {name} = {self.items[name].count}")
            else:
                item = Item(name, base_price, self.tip, self.tax, count)
                self.items[name.lower()] = item

        return self.items

    def prompt_base_price(self, name):
        accepted: bool = False
        base_price: float = None
        while not accepted:
            response: str = input(f"Price of {name}? ")
            if DECIMAL_REGEX.match(response) or response == "0":
                base_price = float(response)
                accepted = True
            elif PERCENTAGE_REGEX.match(response):
                base_price, _ = response.split("%")
                base_price = float(base_price)
                accepted = True
            elif DOLLAR_REGEX.match(response):
                _, base_price = response.split("$")
                base_price = float(base_price)
                accepted = True
            else:
                print(f"Invalid input. Acceptable formats: 18%, 18.0%, 0.18")

        return base_price

    def prompt_paid_by(self) -> str:
        paid_by = input("Who paid? ").title()
        self.paid_by = paid_by
        return self.paid_by

    def calculate_order(self, item_name, count) -> float:
        price = self.items[item_name].price
        return price * count

    def get(self, item_name) -> Item:
        item_name = item_name.lower()
        return self.items[item_name]
