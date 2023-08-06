from datetime import datetime
from unittest import TestCase

import freezegun
from dateutil.parser import parse

from openmodule.config import settings
from openmodule.models.backend import Access, AccessCategory


class AccessModelTestCase(TestCase):
    def assertTzNaive(self, d):
        self.assertTrue(d.tzinfo is None)

    def tearDown(self) -> None:
        super().tearDown()
        settings.reset()

    def is_valid_at(self, access, dt, timezone="Europe/Vienna"):
        dt = parse(dt)
        return access.is_valid_at(dt, timezone)

    def test_deserialized_datetimes_are_timezone_native(self):
        # unix timestamps
        json_bytes = b'{"start": 1600000, "user": "some-user", "category": "booked-digimon"}'
        access = Access.parse_raw(json_bytes)
        self.assertTzNaive(access.start)

        # tz aware iso strings
        json_bytes = b'{"start": "2017-02-15T20:26:08.937881-06:00", "user": "some-user", "category": "booked-digimon"}'
        access = Access.parse_raw(json_bytes)
        self.assertTzNaive(access.start)

        # naive iso strings
        json_bytes = b'{"start": "2017-02-15T20:26:08.937881", "user": "some-user", "category": "booked-digimon"}'
        access = Access.parse_raw(json_bytes)
        self.assertTzNaive(access.start)

    def test_is_valid_non_recurrent_start_end(self):
        access = Access(start="2000-01-02T00:00", end="2000-01-03T00:00", user="test", category="booked-digimon")

        # naive test
        self.assertFalse(self.is_valid_at(access, "2000-01-01T23:59:59"))
        self.assertTrue(self.is_valid_at(access, "2000-01-02T00:00"))
        self.assertTrue(self.is_valid_at(access, "2000-01-03T00:00"))
        self.assertFalse(self.is_valid_at(access, "2000-01-03T00:00:01"))

        # timezone aware test
        self.assertFalse(self.is_valid_at(access, "2000-01-02T01:59+02:00"))
        self.assertTrue(self.is_valid_at(access, "2000-01-02T02:00+02:00"))
        self.assertTrue(self.is_valid_at(access, "2000-01-03T02:00+02:00"))
        self.assertFalse(self.is_valid_at(access, "2000-01-03T02:01+02:00"))

    def test_is_valid_timezone_issue(self):
        access = Access(user="b1", start="2020-01-01 00:00", end="2020-01-01 04:00",
                        category=AccessCategory.booked_digimon)

        with freezegun.freeze_time("2020-01-01 03:30"):
            access = access.parse_raw(access.json_bytes())
            self.assertTrue(access.is_valid_at(datetime.now(), None))

    def test_is_valid_non_recurrent_start_no_end(self):
        access = Access(start="2000-01-02T00:00", user="test", category="booked-digimon")

        # naive test
        self.assertFalse(self.is_valid_at(access, "2000-01-01T23:59:59"))
        self.assertTrue(self.is_valid_at(access, "2000-01-02T00:00"))
        self.assertTrue(self.is_valid_at(access, "3000-02-02T00:00"))

        # timezone aware test
        self.assertFalse(self.is_valid_at(access, "2000-01-01T01:59:59+02:00"))
        self.assertTrue(self.is_valid_at(access, "2000-01-02T02:00+02:00"))
        self.assertTrue(self.is_valid_at(access, "3000-02-02T02:00+02:00"))

    def test_is_valid_non_recurrent_start_end_recurrent(self):
        # TODO
        pass

    def test_is_valid_non_recurrent_start_no_end_recurrent(self):
        # TODO
        pass
