import ctypes
import logging
import threading
import time
from typing import Callable, Optional
from unittest import TestCase

from openmodule.config import override_settings
from openmodule.core import shutdown_openmodule
from openmodule.utils.schema import Schema
from openmodule_test.health import HealthTestMixin
from openmodule_test.zeromq import find_free_port


class InterruptTestMixin(TestCase):
    """
    Helper class for testing interrupts and exceptions in code
    for usage, look at file tests/test_interrupt
    """
    finished = False

    def tearDown(self):
        super().tearDown()
        Schema.to_file()

    @classmethod
    def async_raise(cls, thread_obj, exception):
        found = False
        target_tid = 0
        for tid, tobj in threading._active.items():
            if tobj is thread_obj:
                found = True
                target_tid = tid
                break
        if not found:
            raise ValueError("Invalid thread object")

        ret = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(target_tid),
                                                         ctypes.py_object(exception))
        if ret == 0:
            raise ValueError("Invalid thread ID")
        elif ret > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(target_tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")

    def function_wrapper(self, f):
        def wrapper():
            self.finished = False
            f()
            self.finished = True

        return wrapper

    def wait_for_setup(self):
        pass

    def exception_in_function(self, f, exception, *, raise_exception_after: float = 3.0, shutdown_timeout: float = 3.0):
        thread = threading.Thread(target=self.function_wrapper(f), daemon=True)
        thread.start()
        self.wait_for_setup()
        time.sleep(raise_exception_after)
        self.assertFalse(self.finished)
        self.async_raise(thread, exception)
        logging.error(exception)
        t0 = time.time()
        while time.time() - t0 < shutdown_timeout:
            if thread.is_alive():
                time.sleep(0.5)
            else:
                self.assertTrue(self.finished)

                return
        self.async_raise(thread, SystemExit)
        raise AssertionError("Thread took to long for shutdown")

    def custom_action_in_function(self, f, action, *, call_action_after: float = 3.0, shutdown_timeout: float = 3.0):
        thread = threading.Thread(target=self.function_wrapper(f), daemon=True)
        thread.start()
        self.wait_for_setup()
        time.sleep(call_action_after)
        self.assertFalse(self.finished)
        action(f)
        logging.info(f"action {action.__name__}")
        t0 = time.time()
        while time.time() - t0 < shutdown_timeout:
            if thread.is_alive():
                time.sleep(0.2)
            else:
                self.assertTrue(self.finished)
                return
        self.async_raise(thread, SystemExit)
        raise AssertionError("Thread took to long for shutdown")


@override_settings(BROKER_SUB=f"tcp://127.0.0.1:{find_free_port()}",
                   BROKER_PUB=f"tcp://127.0.0.1:{find_free_port()}")
class MainTestMixin(HealthTestMixin, InterruptTestMixin):
    topics = ["healthz"]

    def wait_for_setup(self):
        self.wait_for_health()

    def tearDown(self):
        try:
            shutdown_openmodule()
        except AssertionError:
            pass
        super().tearDown()
