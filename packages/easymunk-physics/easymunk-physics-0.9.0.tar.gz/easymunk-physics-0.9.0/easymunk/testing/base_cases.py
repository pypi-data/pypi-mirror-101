import pickle
from typing import Iterator, Callable, Tuple

import pytest
import sidekick.api as sk
from hypothesis import given
from hypothesis.core import SearchStrategy

from .utils import description_fixture
from ..core import Space

NOT_GIVEN = object()


class ObjectTestCase:
    """
    Test some easymunk class produced by the given strategy.
    """

    # Enable/disable or let it autodiscover protocols
    pickle = True
    repr = True
    eq = True
    hash = True
    mutable = True
    cls = None

    @classmethod
    def _iter_test_methods(cls) -> Iterator[Tuple[Callable, str, bool]]:
        """
        Yield all pairs of (test func, test name, is comparison test) for class.

        Comparison tests receive two objects as arguments while standard tests
        receive only one.
        """
        for attr in dir(cls):
            if attr.startswith("test_"):
                value = getattr(cls, attr)
                if getattr(value, "is_hypothesis_test", False):
                    continue
                yield (value, attr.startswith("test_cmp_"))

    def __init_subclass__(
        typ, strategy: SearchStrategy = NOT_GIVEN, abstract=False, cls=None
    ):

        if cls is not None:
            typ.cls = cls
        if abstract:
            return  # Abstract base, do not decorate it yet
        if strategy is NOT_GIVEN:
            raise NotImplementedError("must declare a strategy during class creation!")

        if cls is None and isinstance(strategy, type):
            cls = strategy
        elif cls is None:
            cls = typ.cls

        if not cls:
            raise NotImplementedError("must define a target class.")

        for fn, name, is_cmp in typ._iter_test_methods():
            if is_cmp:
                new = given(strategy, strategy)(fn)
            else:
                new = given(strategy)(fn)
            setattr(cls, name, new)

    def test_object_generic_protocols(self, obj):
        if self.pickle:
            self._test_pickle(obj)
        if self.hash:
            self._test_hash(obj)
        if self.repr:
            self._test_repr(obj)

    def _test_pickle(self, obj):
        other = pickle.loads(pickle.dumps(obj))
        assert other == obj

    def _test_hash(self, obj):
        assert len({obj, obj}) == 1
        assert hash(obj) != -1

    def _test_repr(self, obj):
        src = repr(obj)
        assert compile(src, "", "eval"), "repr(obj) must be valid python syntax"

    def test_cmp_object_generic_protocols(self, x, y):
        if self.eq:
            assert x == x and y == y


class PickledObjectTestCase(ObjectTestCase, abstract=True):
    @property
    def attributes(self):
        attrs = {*self.cls._pickle_args, *self.cls._pickle_kwargs}
        return attrs

    pickled_attributes = sk.alias("attributes")

    def _test_pickle(self, obj):
        super()._test_pickle(obj)
        other = pickle.loads(pickle.dumps(obj))

        template = "property {0!r} of pickled object changed from {1!r} to {2!r} "
        for k in self.pickled_attributes:
            orig = getattr(obj, k)
            copy = getattr(other, k)
            assert orig == copy, template.format(k, orig, copy)


class SpaceTestCase:
    """
    A base class that provides initialized spaces with some scenarios useful
    for testing
    """

    has_collision = False
    n_hits = 0

    @description_fixture()
    def sp1(self):
        """
        Two still colliding circles with a small overlap.
        """
        space = Space()
        space.create_circle(1, name="b1", collision_type=1)
        space.create_circle(1, position=(1.75, 0), name="b2", collision_type=2)
        return space

    @description_fixture()
    def sp2(self):
        """
        Two non-colliding circles with same mass.

        Projectile "b1" reaches target "b2" with v=(1, 0) before t=1
        """
        space = Space()
        space.create_circle(1, velocity=(1, 0), name="b1", collision_type=1)
        space.create_circle(1, position=(2.75, 0), name="b2", collision_type=2)
        return space

    @description_fixture()
    def sp3(self):
        """
        A circle "b1" falling into a static line segment "b2" before t=1.

        Segment is in an horizontal line at y=0 and circle starts at (0, 2).
        """
        space = Space(gravity=(0, -4))
        space.create_circle(1, position=(0, 2), name="b1", collision_type=1)
        space.create_segment(
            (-1, 0),
            (1, 0),
            radius=0.25,
            name="b2",
            body_type="static",
            collision_type=2,
        )
        return space

    @description_fixture()
    def sp4(self):
        """
        A triangle "b1" falling into a static line segment "b2" before t=1.

        Segment is in an horizontal line at y=0 and triangle starts at (0, 2).
        """
        space = Space(gravity=(0, -4))
        space.create_regular_poly(3, 1, position=(0, 2), name="b1", collision_type=1)
        space.create_segment(
            (-1, 0),
            (1, 0),
            radius=0.25,
            name="b2",
            body_type="static",
            collision_type=2,
        )
        return space

    @pytest.fixture(params=["sp2", "sp3", "sp4"])
    def sp_will_collide(self, request):
        """
        Parametrize over all pending collision spaces.
        """
        return request.getfixturevalue(request.param)
