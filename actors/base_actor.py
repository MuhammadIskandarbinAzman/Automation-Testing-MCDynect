from typing import List, TypeVar, Type, Dict, Any

"""
This module defines the base Actor class for the Screenplay Pattern.
All specific actors (e.g., Licensee, AreaManager) will inherit from this base.
"""
from typing import List, TypeVar, Type, Dict, Any

T = TypeVar("T")

class Actor:
    """
    The Actor represents a user of the system.
    It has a name and a set of abilities it can use to interact with the system.
    """
    _abilities: Dict[Type, Any]

    def __init__(self, name: str = "Actor"):
        self.name = name
        self._abilities = {}

    def who_can(self, ability: T) -> "Actor":
        """
        Grants the actor a specific ability.
        Example: `Actor().who_can(BrowseTheWeb.with_browser_page(page))`
        """
        self._abilities[type(ability)] = ability
        return self

    def uses_ability(self, ability_type: Type[T]) -> T:
        """
        Retrieves a specific ability for the actor to use.
        Used internally by Tasks and Questions.
        """
        if ability_type not in self._abilities:
            raise ValueError(f"{self.name} does not have the ability {ability_type.__name__}")
        return self._abilities[ability_type]

    def attempts_to(self, *tasks: Any) -> None:
        """
        Instructs the actor to perform one or more tasks.
        Example: `the_licensee.attempts_to(Login.with_credentials("email", "password"))`
        """
        for task in tasks:
            task.perform_as(self)

    def asks_for(self, question: Any) -> Any:
        """
        Asks the actor to answer a question using their abilities.
        Example: profile = the_licensee.asks_for(GetProfileInfo())
        """
        return question.answered_by(self)
