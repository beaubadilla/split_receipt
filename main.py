from typing import List

from Receipt import Receipt
from SplitReceipt import SplitReceipt
from split_receipt import Person


def main():
    app = SplitReceipt()

    people: List[Person] = app.prompt_people()

    receipt = app.prompt_receipt_details()
    # orders = app.prompt_orders()
    # print(app.summary())


if __name__ == "__main__":
    main()
