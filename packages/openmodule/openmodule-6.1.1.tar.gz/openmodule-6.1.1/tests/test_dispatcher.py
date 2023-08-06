from functools import partial
from typing import Any
from unittest import TestCase

from openmodule.config import settings
from openmodule.dispatcher import MessageDispatcher
from openmodule.models.base import ZMQMessage


class MessageDispatcherBaseTest(TestCase):
    dispatcher: MessageDispatcher
    message: Any

    def dummy_message(self, type="test", **kwargs):
        return {"type": type, "name": "testclient", **kwargs}

    def _set_true_handler(self, message, var="message"):
        """test handler"""
        setattr(self, var, message)

    def setUp(self):
        super().setUp()
        self.dispatcher = MessageDispatcher()
        self.message = None

    def tearDown(self) -> None:
        settings.reset()
        super().tearDown()


class MessageDispatcherBasicsTestCase(MessageDispatcherBaseTest):
    def test_topic_is_str(self):
        self.dispatcher.register_handler("test", ZMQMessage, self._set_true_handler)
        self.assertIsNone(self.message)

        self.dispatcher.dispatch(b"test", self.dummy_message())
        self.assertIsNotNone(self.message)

    def test_no_filter(self):
        self.dispatcher.register_handler(b"test", ZMQMessage, self._set_true_handler)
        self.assertIsNone(self.message)

        self.dispatcher.dispatch(b"test", self.dummy_message())
        self.assertIsNotNone(self.message)

    def test_filter(self):
        self.dispatcher.register_handler(b"test", ZMQMessage, self._set_true_handler, filter={"type": "some-type"})

        # filter does not match
        self.dispatcher.dispatch(b"test", self.dummy_message(type="incorrect"))
        self.assertIsNone(self.message)

        # filter matches
        self.dispatcher.dispatch(b"test", self.dummy_message("some-type"))
        self.assertIsNotNone(self.message)

    def test_multiple_filter(self):
        # multiple handlers with identical filters and topics are allowed
        self.message1 = None
        self.message2 = None

        self.dispatcher.register_handler(b"test", ZMQMessage, partial(self._set_true_handler, var="message1"),
                                         filter={"type": "some-type"})
        self.dispatcher.register_handler(b"test", ZMQMessage, partial(self._set_true_handler, var="message2"),
                                         filter={"type": "some-type"})

        # filter does not match
        self.dispatcher.dispatch(b"test", self.dummy_message(type="incorrect"))
        self.assertIsNone(self.message1)
        self.assertIsNone(self.message2)

        # filter matches
        self.dispatcher.dispatch(b"test", self.dummy_message("some-type"))
        self.assertIsNotNone(self.message1)
        self.assertIsNotNone(self.message2)

    def test_prefix_does_not_match(self):
        # since zmq subscribes on all topics as prefixes, the dispatcher
        # has to full-match the topic
        self.dispatcher.register_handler(b"test", ZMQMessage, self._set_true_handler)
        self.dispatcher.dispatch(b"testp", self.dummy_message())
        self.assertIsNone(self.message)

        # exact match works
        self.dispatcher.dispatch(b"test", self.dummy_message())
        self.assertIsNotNone(self.message)


class MessageDispatcherWithoutExecutorTestCase(MessageDispatcherBaseTest):
    def test_exception_in_handler(self):
        def raises_exception(message):
            raises_exception.register_schema = False
            raise Exception("something broke!")

        self.dispatcher.register_handler(b"test", ZMQMessage, raises_exception, register_schema=False)
        with self.assertLogs() as cm:
            self.dispatcher.dispatch(b"test", self.dummy_message())
        self.assertIn("something broke!", cm.output[0])

    def test_validation_error(self):
        def handler(x): None

        handler.register_schema = False
        self.dispatcher.register_handler("test", ZMQMessage, handler, register_schema=False)
        with self.assertLogs() as cm:
            self.dispatcher.dispatch(b"test", {})
        self.assertIn("validation error", cm.output[0])
