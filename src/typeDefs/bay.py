from typing import TypedDict, Optional


class IBay(TypedDict):
    id: int
    name: str
    bayNumber: str
    stationName: str
    bayType: str
    voltage: str