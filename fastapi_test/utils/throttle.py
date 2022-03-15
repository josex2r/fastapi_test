from functools import partial
from threading import Timer
from typing import Callable


class ThrottleWrapper:
    _timer: Timer

    def __init__(self, func: Callable, milliseconds: int) -> None:
        self._func = func
        self._milliseconds = milliseconds

    @property
    def has_timer(self):
        return hasattr(self, "_timer") and self._timer is not None

    @property
    def timer_is_alive(self):
        return self._timer and self._timer.is_alive()

    @property
    def is_running(self):
        return self.has_timer and self.timer_is_alive

    def next_tick(self):
        if self._nextCallback is not None:
            self._nextCallback()
            self._nextCallback = None
            self._timer = Timer(self._milliseconds / 1000, self.next_tick)
            self._timer.start()

    def __call__(self, *args, **kwargs) -> None:
        self._nextCallback = partial(self._func, *args, **kwargs)

        if not self.is_running:
            self.next_tick()


def throttle(milliseconds: int) -> Callable:
    """
    Decorator to throttle a function X milliseconds
    """

    def decorator(func: Callable) -> ThrottleWrapper:
        return ThrottleWrapper(func, milliseconds)

    return decorator
