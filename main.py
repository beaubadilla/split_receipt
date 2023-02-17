from typing import List

from Receipt import Receipt
from SplitReceipt import SplitReceipt
from split_receipt import Person


def main():
    app = SplitReceipt()

    # Get all involved people
    people: List[Person] = app.prompt_people()

    # Get details of all receipts
    ## Create events
    ## Create items
    app.prompt_receipt_details()

    # Get all orders
    orders = app.prompt_orders()
    orders_info = app.parse_orders()

    # For each order,
    # populate each person's info
    for names, kw, items in orders_info:
        if kw == "got":
            app.add_individual_purchase(names, items)
        elif kw == "shared":
            app.add_split_purchase(names, items)
        elif kw == "covered":
            app.add_communal_purchase(names, items)

    # For each person,
    # retrieve summary
    ## for each event, print personal "receipt"


if __name__ == "__main__":
    main()
