from __future__ import annotations

from typing import *
from uuid import uuid1

from ecstremity.registries import (ComponentRegistry, EntityRegistry,
                                   PrefabRegistry, QueryRegistry)

if TYPE_CHECKING:
    from ecstremity import Component, Entity

    from .prefab import Prefab
    from .query import Query


GAME = TypeVar("GAME")


class Engine:

    def __init__(self) -> None:
        self.components = ComponentRegistry(self)
        self.entities = EntityRegistry(self)
        self.prefabs = PrefabRegistry(self)
        self.queries = QueryRegistry(self)

    @staticmethod
    def generate_uid() -> str:
        """Generate a new unique identifier for an `Entity`."""
        return uuid1().hex

    def get_entity(self, uid: str) -> Entity:
        """Use a `uid` to return an `Entity` from the `EntityRegistry`."""
        return self.entities.get(uid)

    def create_component(
            self,
            component: Union[str, Component],
            properties: Dict[str, Any]
        ) -> Component:
        """Initialize a new component from those registered using the
        specified properties.
        """
        return self.components.create(component, properties)

    def create_entity(self, uid: Optional[str] = None) -> Entity:
        """Use the `EntityRegistry` to create a new `Entity` with the
        specified `uid`.
        """
        return self.entities.create(uid)

    def create_prefab(self, name_or_class, initial_props=None):
        """Use the `PrefabRegistry` to initialize a set of new components
        using the specified properties."""
        return self.prefabs.create(name_or_class)

    def create_query(
            self,
            any_of: Optional[List[str]] = None,
            all_of: Optional[List[str]] = None,
            none_of: Optional[List[str]] = None
        ) -> Query:
        return self.queries.create(any_of=any_of, all_of=all_of, none_of=none_of)

    def destroy_entity(self, uid: str) -> None:
        self.entities.destroy(uid)

    def register_component(self, component: Component) -> None:
        """Register a component class to the ComponentRegistry."""
        self.components.register(component)

    def register_prefab(self, definition) -> None:
        self.prefabs.register(definition)


class EngineAdapter(Engine):

    def __init__(self, *, client: GAME) -> None:
        self.client = client
        super().__init__()
