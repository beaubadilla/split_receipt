from typing import List

from Person import Person


class Squad:
    def __init__(self) -> None:
        self.squad = {}

    def add(self, person: Person, overwrite=False) -> None:
        if person.name in self.squad and not overwrite:
            raise ValueError(
                f"{person.name} already in the squad.\n"
                f"1) Set 'overwrite' to True to always overwrite.\n"
                f"2) Someone may have the same name, so use a unique name.\n"
            )
        else:
            self.squad[person.name] = person

    def get(self, name: str) -> Person:
        return self.squad[name] if name in self.squad else ""
