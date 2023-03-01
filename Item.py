from dataclasses import dataclass


@dataclass
class Item:
    name: str
    base_price: float
    tip: float = 0
    tax: float = 0
    _count: int = 0
    add_ons: ... = None
    description: str = None

    def __str__(self) -> str:
        return f"{self.name} costs {self.base_price} before {self.tax} tax and {self.tip} tip"

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, val: int):
        self._count += val

    @property
    def price(self):
        return (
            self.base_price
            + (self.tax * self.base_price)
            + (self.tip * self.base_price)
        )
