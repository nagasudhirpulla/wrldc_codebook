from typing import TypedDict
import datetime as dt


class IUnRevOutage(TypedDict):
    rtoId: int
    elTypeId: int
    elId: int
    elType: str
    outageType: str
    elName: str
    outageDt: str
    reason: str
    outageTag: str
    outageRemarks: str
