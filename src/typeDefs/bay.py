from src.typeDefs.element import IElement


class IBay(IElement):
    bayNumber: str
    stationName: str
    bayType: str
    voltage: str
