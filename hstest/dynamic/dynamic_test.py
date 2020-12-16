import inspect
from typing import Any, List

from hstest.dynamic.input.dynamic_testing import DynamicTestElement
from hstest.stage_test import StageTest
from hstest.test_case import DEFAULT_TIME_LIMIT


def dynamic_test(func=None, *,
                 order: int = 0,
                 time_limit: int = DEFAULT_TIME_LIMIT,
                 data: List[Any] = None,
                 repeat: int = 1):
    """
    Decorator for creating dynamic tests
    """

    class DynamicTestingMethod:
        def __init__(self, fn):
            self.fn = fn

        def __set_name__(self, owner, name):
            # do something with owner, i.e.
            # print(f"Decorating {self.fn} and using {owner}")
            self.fn.class_name = owner.__name__

            if not issubclass(owner, StageTest):
                setattr(owner, name, self.fn)
                return

            # then replace ourself with the original method
            setattr(owner, name, self.fn)

            methods: List[DynamicTestElement] = StageTest._dynamic_methods.get(owner, [])
            methods += [
                DynamicTestElement(lambda *a, **k: self.fn(*a, **k),
                                   self.fn.__name__, (order, len(methods)), repeat, time_limit, data)
            ]
            owner._dynamic_methods[owner] = methods

    is_method = inspect.ismethod(func)
    is_func = inspect.isfunction(func)
    if is_method or is_func:
        # in case it is called as @dynamic_test
        return DynamicTestingMethod(func)

    # in case it is called as @dynamic_test(...)
    return DynamicTestingMethod
