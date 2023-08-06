from typing import Optional, List, Iterable, Union

from openmodule.models.backend import MediumType
from openmodule.models.base import OpenModuleModel


def _truncate(x):
    if len(x) > 10:
        return x[:10] + "..."
    else:
        return x


class Medium(OpenModuleModel):
    id: str
    type: MediumType

    def __str__(self):
        return f"{self.type}:{_truncate(self.id)}"


class QRMedium(Medium):
    type: MediumType = "qr"


class PINMedium(Medium):
    type: MediumType = "pin"


class NFCMedium(Medium):
    type: MediumType = "nfc"


class RegexMedium(Medium):
    type: MediumType = "regex"


class LPRCountry(OpenModuleModel):
    code: str
    state: str = ""
    confidence: float = 1


class LPRAlternative(OpenModuleModel):
    confidence: float
    plate: str


class LPRMedium(Medium):
    type: str = "lpr"
    country: LPRCountry = LPRCountry(code="OTHER")
    confidence: float = 1
    alternatives: List[LPRAlternative] = []

    def __str__(self):
        return f"{self.type}:[{self.country.code}]{_truncate(self.id)}"


class Vehicle(OpenModuleModel):
    id: int
    lpr: Optional[LPRMedium]
    qr: Optional[Medium]
    nfc: Optional[Medium]
    pin: Optional[Medium]

    def iterate_media(self) -> Iterable[Union[Medium, LPRMedium]]:
        """
        an iterable of all media of this vehicle
        """
        if self.lpr:
            yield self.lpr
        if self.qr:
            yield self.qr
        if self.nfc:
            yield self.nfc
        if self.pin:
            yield self.pin

    def __str__(self):
        media = ", ".join(str(x) for x in [self.lpr, self.qr, self.nfc] if x)
        if media:
            media = ", " + media
        return f"Vehicle<id:{str(self.id)[-7:]}{media}>"
