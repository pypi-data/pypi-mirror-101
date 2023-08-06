import logging
import time
from unittest import TestCase

from openmodule.config import settings
from openmodule.core import init_openmodule, shutdown_openmodule
from openmodule_test.interrupt import InterruptTestMixin, MainTestMixin


def test():
    try:
        test.run = True
        t0 = time.time()
        while test.run and time.time() - t0 < 10:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Keyboard")
    except Exception as e:
        logging.info(f"exception: {e}")
    else:
        logging.info("not running")
    finally:
        logging.info("killed")


class InterruptTest(InterruptTestMixin, TestCase):
    def test_exception(self):
        with self.assertLogs() as cm:
            self.exception_in_function(test, Exception("some-exception"))
        self.assertIn("some-exception", str(cm.output))

    def test_keyboard(self):
        with self.assertLogs() as cm:
            self.exception_in_function(test, KeyboardInterrupt)
        self.assertIn("Keyboard", str(cm.output))

    def test_run(self):
        with self.assertLogs() as cm:
            self.custom_action_in_function(test, self.action)
        self.assertIn("not running", str(cm.output))

    def action(self, callable):
        callable.run = False


def sleepy():
    try:
        t0 = time.time()
        while time.time() - t0 < 10:
            time.sleep(1)
    except Exception:
        sleepy()


class InterruptTimeoutTest(InterruptTestMixin, TestCase):
    function = staticmethod(sleepy)

    def test_exception(self):
        with self.assertRaises(AssertionError) as e:
            self.exception_in_function(sleepy, Exception())
        self.assertIn("Thread took to long for shutdown", str(e.exception))


def main():
    core = init_openmodule(settings)
    main.run = True
    try:
        while main.run:
            time.sleep(1)
        logging.info("stopped")
    except KeyboardInterrupt:
        logging.error("keyboard")
    except Exception as e:
        print(e)
    finally:
        shutdown_openmodule()


class MainTest(MainTestMixin):
    def test_keyboard(self):
        with self.assertLogs() as cm:
            self.exception_in_function(main, KeyboardInterrupt)
        self.assertIn("keyboard", str(cm.output))

    def test_run(self):
        def stop(f):
            logging.error(f)
            f.run = False

        with self.assertLogs() as cm:
            self.custom_action_in_function(main, stop)
        self.assertIn("stopped", str(cm.output))