from threading import Timer
from typing import Callable


class DebounceWrapper:
    _timer: Timer

    def __init__(self, func: Callable, milliseconds: int) -> None:
        self._func = func
        self._milliseconds = milliseconds

    def __call__(self, *args, **kwargs) -> None:
        try:
            self._timer.cancel()
        except AttributeError:
            pass

        self._timer = Timer(self._milliseconds / 1000.0,
                            self._func, args, kwargs)
        self._timer.start()


def debounce(milliseconds: int) -> Callable:
    """
    Decorator to debounce a function X milliseconds
    """
    def decorator(func: Callable) -> DebounceWrapper:
        return DebounceWrapper(func, milliseconds)

    return decorator
