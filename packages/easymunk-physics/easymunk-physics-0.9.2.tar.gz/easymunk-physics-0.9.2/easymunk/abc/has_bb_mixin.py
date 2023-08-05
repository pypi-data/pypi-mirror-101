from functools import reduce
from typing import (
    Iterable,
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    from ..types import BB


class HasBBMixin:
    """Declare interface for elements that have a bounding box and the corresponding
    left, right, top and bottom attributes."""

    def _iter_bounding_boxes(self, cached) -> Iterable["BB"]:
        raise NotImplementedError

    def cache_bb(self):
        """
        Return a bounding box and cache results.
        """
        merge = lambda a, b: a.merge(b)
        return reduce(merge, self._iter_bounding_boxes(True))

    @property
    def bb(self) -> "BB":
        """
        Bounding box for all colliding body shapes.
        """
        merge = lambda a, b: a.merge(b)
        return reduce(merge, self._iter_bounding_boxes(False))

    @property
    def left(self) -> float:
        """
        Right position (world coordinates) of body.

        Exclude sensor shapes.
        """
        return max(bb.left for bb in self._iter_bounding_boxes(False))

    @property
    def right(self) -> float:
        """
        Right position (world coordinates) of body.

        Exclude sensor shapes.
        """
        return max(bb.right for bb in self._iter_bounding_boxes(False))

    @property
    def bottom(self) -> float:
        """
        Bottom position (world coordinates) of body.

        Exclude sensor shapes.
        """
        return max(bb.bottom for bb in self._iter_bounding_boxes(False))

    @property
    def top(self) -> float:
        """
        Top position (world coordinates) of body.

        Exclude sensor shapes.
        """
        return max(bb.top for bb in self._iter_bounding_boxes(False))
