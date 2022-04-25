#!/usr/bin/python3
# TODO: color terminal
# TODO: create test suite
# TODO: fix "could not find brian/allen"
# TODO: fix check_subtotal
# TODO: all "all" option for even-split function
# TODO: tip, tax, fees, etc into a list so it can be adaptable
#       requires another prompt
# TODO: add some type of "fix previous error"
#       possible implementation: have a history class/list
# TODO: refactor to class SplitReceipt
#       e.g.
#       class SplitReceipt():
#           ...
#       def main():
#           sr = SplitReceipt()
#           sr.get_people()
#           sr.get_receipt_details()
#           sr.get_peoples_purchases()
#           ...
# TODO: have each person separate, then in the end, prompt if anyone is under one request.
#   covers edge cases where a couple participates, but one of them only participates in one
#   event (if theres 2+) and that event is even split. currently, even split assumes entire
#   couple
#   EDIT: well actually, I could just keep the same implementation and simply just not put them
#       in a pair. Doing it the way mentioned above COULD involve a lot of prompts. Didn't think too hard

TAB = '\t'
def main():
    # People that need to I need to request money from
    people = get_people()

    # ask how many transactions(i.e. receipts)
    num_transactions = int(
        input(f"{bcolors.BLUE}How many transactions? {bcolors.ENDC}") or 1
    )
    all_events = {}
    for i in range(num_transactions):
        # TODO: char limit for easier indent formatting?
        event = input(f"\t{bcolors.ORANGE}Event? {bcolors.ENDC}")

        # TODO: dupe events presents a problem
        all_events[event] = {}

        subtotal = float(input(f"\t{bcolors.YELLOW}Subtotal? {bcolors.ENDC}"))
        tax_perc = get_tax(subtotal)
        tip_perc = get_tip(subtotal)
        all_events[event]["tax"] = tax_perc
        all_events[event]["tip"] = tip_perc

        # If this transaction is evenly split, everyone's price is equal
        is_even_split = input(
            f"\t{bcolors.YELLOW}Even split for this transction?(y/n): {bcolors.ENDC}"
        ).lower()
        if is_even_split == "y":
            purchase = input(f"\t{bcolors.YELLOW}Purchase? {bcolors.ENDC}")

            ids_involved = prompt_people_menu(event, people)

            num_ids = calculate_num_ids(ids_involved, people)

            for id in ids_involved:
                price_per_person = calculate_price_per_person(
                    subtotal, num_ids, people, id
                )
                people[id].add_purchase(
                    event, purchase, price_per_person, tax_perc, tip_perc
                )
        else:  # transaction is not evenly split
            print(
                f"\t\t{bcolors.PURPLE}Enter all purchases. Enter DONE when finished.{bcolors.ENDC}"
            )
            while True:
                purchase_details = input(
                    f"\t\t{bcolors.PURPLE}Purchase, price, and name(s)?{bcolors.ENDC} "
                ).split()
                if purchase_details[0] == "DONE":
                    break

                purchase = purchase_details[0]
                purchasers = purchase_details[-1].split(",")
                price = float(purchase_details[1])

                # Multiple people bought the same item
                if len(purchasers) > 1:
                    is_ppp = input(
                        f"\t\t\t{bcolors.PURPLE}Is this price per person?(y/n){bcolors.ENDC} "
                    )
                    if is_ppp == "n":
                        price = price / len(purchasers)

                found = set()
                for purchaser in purchasers:
                    split_purchasers = []
                    if "/" in purchaser:
                        split_purchasers = purchaser.split("/")
                    for p in people:
                        if split_purchasers:
                            for split_purchaser in split_purchasers:
                                if split_purchaser == p.name:
                                    p.add_purchase(
                                        event,
                                        "1/2 " + purchase,
                                        price / len(split_purchasers),
                                        tax_perc,
                                        tip_perc,
                                    )
                                    found.add(split_purchaser)
                        else:
                            if purchaser == p.name:
                                p.add_purchase(
                                    event, purchase, price, tax_perc, tip_perc
                                )
                                found.add(purchaser)
                                break
                not_found = set(purchasers) - found
                not_found = " ".join(list(not_found))
                if not_found:
                    print(
                        f"\t\t\t{bcolors.FAIL}Could not find {not_found}{bcolors.ENDC}"
                    )

            # TODO: convert into func
            check_subtotal = sum(
                [
                    person.purchases[event]["total"]
                    for person in people
                    if event in person.purchases
                ]
            )
            if check_subtotal < subtotal + 0.01 and check_subtotal > subtotal - 0.01:
                print(
                    f"{bcolors.GREEN}SUBTOTAL FOR {event.upper()} MATCHES RECEIPT{bcolors.ENDC}"
                )
            else:
                if check_subtotal < subtotal:
                    print(
                        f"\t{bcolors.FAIL}Missing purchases for {event}. Subtotal={subtotal}, found={check_subtotal}{bcolors.ENDC}"
                    )
                elif check_subtotal > subtotal:
                    print(
                        f"\t{bcolors.FAIL}Too many purchases / incorrect price for purchase(s). Subtotal={subtotal}, found={check_subtotal}{bcolors.ENDC}"
                    )

    print("Split Receipt Finished")

    max_len_name = max(len(person.name) for person in people)
    MAX_CHAR_COL = 7  # based on observation. subject to change
    max_tabs = int(max_len_name / MAX_CHAR_COL)
    line = ""
    sorted_events = sorted(all_events)
    for i, event in enumerate(sorted_events):
        if i % 2 == 0:
            line += f"{bcolors.ORANGE}{event}\t{bcolors.ENDC}"
        else:
            line += f"{bcolors.YELLOW}{event}\t{bcolors.ENDC}"

    print(f"Event:{TAB * max_tabs}{line}")

    line = ""
    for i, event in enumerate(sorted_events):
        if i % 2 == 0:
            line += f'{bcolors.ORANGE}{all_events[event]["tax"] * 100:.2f}%\t{bcolors.ENDC}'
        else:
            line += f'{bcolors.YELLOW}{all_events[event]["tax"] * 100:.2f}%\t{bcolors.ENDC}'
    print(f"(Tax:{TAB * max_tabs}{line})")

    line = ""
    for i, event in enumerate(sorted_events):
        if i % 2 == 0:
            line += f'{bcolors.ORANGE}{all_events[event]["tip"] * 100:.2f}%\t{bcolors.ENDC}'
        else:
            line += f'{bcolors.YELLOW}{all_events[event]["tip"] * 100:.2f}%\t{bcolors.ENDC}'
    print(f"(Tip:{TAB * max_tabs}{line})")


    for person in people:
        len_name = len(person.name)
        if len_name <= 7: num_tabs = 2
        else: num_tabs = 1
        # If len(name) <= 7
        # if len(name) == 15, len <= 7 needs 2 tabs, else 1 tab
        orders = "("
        # line = f"{bcolors.BLUE}{person.name}\t{bcolors.ENDC}"
        line = f"{bcolors.BLUE}{person.name}{TAB * num_tabs}{bcolors.ENDC}"

        num_events = 0
        for event in sorted_events:
            curr_order = ''
            if num_events % 2 == 0:
                line += bcolors.ORANGE
            else:
                line += bcolors.YELLOW

            if event in person.purchases:
                line += f"${round(person.purchases[event]['total'], 2):.2f}{TAB}"
                # line += "$" + str(round(person.purchases[event]["total"], 2)) + "\t"
            else:
                line += "N/A" + "\t"
            if event in person.purchases:
                curr_order = ", ".join(person.purchases[event]["orders"])
                orders += curr_order

            # if orders is more than just '(', otherwise it
            # could result in '(, fries)'
            if len(curr_order) > 1:
                orders += ", "

            line += bcolors.ENDC
            num_events += 1
        orders += ")"
        line += f"{bcolors.GREEN}" f"${person.total:.2f}" f"{bcolors.ENDC}"
        print(f"{line}{bcolors.PURPLE} {orders}{bcolors.ENDC}")


def get_people():
    return [
        Person(person)
        for person in sorted(
            input(f"{bcolors.BLUE}List of people: {bcolors.ENDC}").split()
        )
    ]


def get_tax(subtotal):
    tax = float(input(f"\t{bcolors.YELLOW}Tax? {bcolors.ENDC}"))
    tax_perc = round(tax / subtotal, 4)
    print(f"\t\t{bcolors.YELLOW}Tax % = {tax_perc * 100:.2f}%{bcolors.ENDC}")
    return tax_perc


def get_tip(subtotal):
    tip = float(input(f"{bcolors.YELLOW}\tTip? {bcolors.ENDC}"))
    tip_perc = round(tip / subtotal, 4)
    print(f"\t\t{bcolors.YELLOW}Tip % = {tip_perc * 100:.2f}%{bcolors.ENDC}")
    return tip_perc


def prompt_people_menu(event, people):
    temp = "\n\t".join([f"{person.id + 1}. {person.name}" for person in people])
    prompt = f"\n\tWho took part in {event}? "
    return [
        int(id) - 1
        for id in input(
            f"{bcolors.YELLOW}"
            f"\tPeople Menu\n"
            f"\t{temp}"
            f"{prompt}"
            f"{bcolors.ENDC}"
        ).split()
    ]


def calculate_num_ids(ids_involved, people):
    count = 0
    # For multiple people under one name (i.e couples)
    for id in ids_involved:
        count += len(
            people[id].name.split("+")
        )  # ok even if the name does not have a '+'
    return count


def calculate_price_per_person(subtotal, num_ids, people, id):
    """Only meant for even split feature"""
    price_per_person = subtotal / num_ids
    # if multiple people under one name, account that in the price
    if "+" in people[id].name:
        price_per_person = price_per_person * len(people[id].name.split("+"))
    return price_per_person


class Person:
    count = 0

    def __init__(self, name):
        self._name = name
        self._total = 0
        self.purchases = {}
        self.id = Person.count
        Person.count += 1

    def __str__(self):
        return f"{self.name} ordered {self.purchases} totaling to {self.total}"

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


# https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
# https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences
# https://en.wikipedia.org/wiki/ANSI_escape_code
class bcolors:
    PURPLE = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    RED = "\033[31m"
    TEST = (
        "\033[38;5;82m"
    )  # [;;<FG color>m, look at https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797 "256 colors"
    PINK = "\033[38;5;213m"
    YELLOW = "\033[38;5;226m"
    ORANGE = "\033[38;5;208m"


if __name__ == "__main__":
    print(
        f"{bcolors.UNDERLINE}{bcolors.PINK}Hello, This is a tool to split receipts.{bcolors.ENDC}"
    )
    main()

# Future
# Incorporate Venmo/Zelle API
