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
    expectedRevDt: str
    reason: str
    outageTag: str
    outageRemarks: str


class IUnRevOutageWithCode(TypedDict):
    rtoId: int
    elTypeId: int
    elId: int
    elType: str
    outageType: str
    elName: str
    outageDt: str
    expectedRevDt: str
    reason: str
    outageTag: str
    outageRemarks: str
    code: str
