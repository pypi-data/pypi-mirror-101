from enum import Enum

from datetime import datetime
from dateutil import rrule, tz
from dateutil.tz import UTC
from dateutil.utils import default_tzinfo
from pydantic import validator, Field
from typing import List, Optional

from openmodule import config
from openmodule.models.base import OpenModuleModel, ZMQMessage, Gateway, timezone_validator, datetime_to_timestamp


class MediumType(str, Enum):
    lpr = "lpr"
    nfc = "nfc"
    pin = "pin"
    qr = "qr"


class AccessCategory(str, Enum):
    booked_digimon = "booked-digimon"
    booked_employee = "booked-employee"
    booked_visitor = "booked-visitor"
    permanent_digimon = "permanent-digimon"
    permanent_employee = "permanent-employee"
    filler_employee = "filler-employee"
    filler_digimon = "filler-digimon"
    filler_visitor_button = "filler-visitor-button"
    filler_visitor_unexpected = "filler-visitor-unexpected"
    unknown_category = "unknown-category"


class AccessRequest(OpenModuleModel):
    """
    The AccessRequest Model
    """
    name: str
    gateway: Optional[Gateway] = None
    medium_type: MediumType
    id: str


def check_recurrence(cls, recurrence, values, **kwargs):
    if recurrence:
        if not values.get("duration"):
            raise ValueError("set a duration when using recurrence")

        try:
            if "DTSTART" not in recurrence:
                raise ValueError("recurrence must contain a DTSTART field")
            if "\n" not in recurrence:
                raise ValueError("DTSTART must be separated by a newline '\\n' character")

            rrule.rrulestr(recurrence)
        except Exception as e:
            raise ValueError(f"recurrence is not valid '{e}'") from None
        return recurrence
    else:
        return None


class Access(OpenModuleModel):
    category: AccessCategory
    start: datetime
    end: Optional[datetime] = None
    duration: Optional[int] = Field(description="duration in seconds, starting with the start time of the "
                                                "recurrence. Required if recurrence is set.")
    recurrence: Optional[str]
    zone: Optional[str]
    occupant_check: bool = False
    infos: Optional[dict] = {}
    user: str

    _check_recurrence = validator("recurrence", allow_reuse=True)(check_recurrence)
    _tz_start = timezone_validator("start")
    _tz_end = timezone_validator("end")

    def dict(self, **kwargs):
        data = super().dict(**kwargs)
        data["start"] = datetime_to_timestamp(data["start"])
        if data.get("end") is not None:
            data["end"] = datetime_to_timestamp(data["end"])
        return data

    def is_valid_at(self, dt, timezone):
        if dt.tzinfo:
            dt = dt.astimezone(UTC).replace(tzinfo=None)
        if self.recurrence:
            assert False, "recurrent accesses are not yet supported"
        else:
            if self.end:
                return self.start <= dt <= self.end
            else:
                return self.start <= dt


class MediumAccesses(OpenModuleModel):
    accesses: List[Access]
    id: str
    type: str


class AccessResponse(OpenModuleModel):
    success: bool = False
    medium: MediumAccesses


class CountMessage(ZMQMessage):
    resource: str = config.resource()
    user: str
    gateway: Gateway
    medium_type: MediumType
    id: str
    count: int
    transaction_id: str
    zone: str
    category: AccessCategory
    real: bool
    access_data: Optional[dict]
    error: Optional[str]
    previous_transaction_id: Optional[List[str]]  # double_entry, choose_random error
    previous_user: Optional[str]  # user_changed error
    previous_medium_type: Optional[str]  # medium_changed, medium_id_changed error
    previous_id: Optional[str]  # medium_changed, medium_id_changed error
    chosen: Optional[dict]  # choose_random error
