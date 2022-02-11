from typing import TypedDict
import datetime as dt


class IRealTimeOutage(TypedDict):
    rtoId: int
    elTypeId: int
    elId: int
    elType: str
    outageType: str
    elName: str
    outageDt: dt.datetime
    reason: str
    outageTag: str
    outageRemarks: str
    revivalDt: dt.datetime
    revivalRemarks: str
