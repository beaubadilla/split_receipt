from dataclasses import dataclass


@dataclass
class Item:
    price: float
    name: str
    _count: int
    add_ons: ... = None
    description: str = None

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, val: int):
        self._count += val
