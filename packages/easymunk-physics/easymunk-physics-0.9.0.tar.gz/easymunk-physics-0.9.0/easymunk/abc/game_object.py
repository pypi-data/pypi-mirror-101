from abc import ABC, abstractmethod
from typing import Any, TypeVar, Optional

GOType = TypeVar("GOType", bound="GameObjectInterface")


class GameObjectInterface(ABC):
    """
    A game object is a composable element in game.
    """

    _parent: Optional[GOType] = None

    def __init_subclass__(cls, **kwargs):
        cls._message_handlers_cache = {}
        super().__init_subclass__(**kwargs)

    @abstractmethod
    def _iter_game_object_children(self):
        raise NotImplementedError

    def draw(self: GOType, camera: Any = None) -> GOType:
        """
        Draw object using the given camera.

        The default implementation is empty. THis method is useful to integrate
        with game libraries with a canvas-like rendering metaphor.
        """
        return self

    def step(self: GOType, dt: float) -> GOType:
        """
        Update object by evolving a single step of duration dt.

        Args:
            dt: Duration of time step.
        """
        for child in self._iter_game_object_children():
            child.step(dt)
        return self

    def process_message(self, msg, /, *args, sender=None):
        """
        Process message.

        The default implementation seeks for a method named handle_<msg>_message()
        and execute it forwarding any positional arguments. The sender object
        is passed as a keyword argument and other keyword arguments can be
        either forwarded or influence the way the message is processed.
        """
        try:
            fn = self._message_handlers_cache[msg]
        except KeyError:
            msg = msg.replace("-", "_")
            name = f"handler_{msg}_message"
            cls = type(self)
            fn = self._message_handlers_cache[msg] = getattr(cls, name)
        fn(self, sender, *args)

    def send_message(self, msg, *args, **kwargs):
        """
        Send message to parent.
        """
        kwargs.setdefault("sender", self)
        self._parent.send(msg, *args, **kwargs)
