import time
from unittest import mock

from fastapi_test.utils.debounce import debounce

spy = mock.Mock()


@debounce(200)
def subject_fn():
    spy()


def test_debounce():
    subject_fn()
    # this smells like shit, must learn to stub "Timer"
    time.sleep(0.21)

    assert spy.call_count == 1

    subject_fn()
    subject_fn()
    subject_fn()
    time.sleep(0.1)

    assert spy.call_count == 1

    time.sleep(0.1)

    assert spy.call_count == 2
