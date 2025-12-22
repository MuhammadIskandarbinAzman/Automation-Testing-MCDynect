from typing import List, TypeVar, Type, Dict, Any

T = TypeVar("T")

class Actor:
    _abilities: Dict[Type, Any]

    def __init__(self, name: str = "Actor"):
        self.name = name
        self._abilities = {}

    def who_can(self, ability: T) -> "Actor":
        self._abilities[type(ability)] = ability
        return self

    def uses_ability(self, ability_type: Type[T]) -> T:
        if ability_type not in self._abilities:
            raise ValueError(f"{self.name} does not have the ability {ability_type.__name__}")
        return self._abilities[ability_type]

    def attempts_to(self, *tasks: Any) -> None:
        for task in tasks:
            task.perform_as(self)

