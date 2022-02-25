import time
from unittest import mock

from fastapi_test.utils.throttle import throttle

spy = mock.Mock()


@throttle(200)
def subject_fn():
    spy()


def test_throttle():
    subject_fn()

    assert spy.call_count == 1

    subject_fn()
    subject_fn()

    assert spy.call_count == 1

    # this smells like shit, must learn to stub "Timer"
    time.sleep(0.21)

    subject_fn()

    assert spy.call_count == 2

    time.sleep(0.21)

    subject_fn()

    assert spy.call_count == 3

    subject_fn()

    time.sleep(0.11)

    assert spy.call_count == 3

    subject_fn()

    time.sleep(0.21)

    assert spy.call_count == 4
