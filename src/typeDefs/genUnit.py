from src.typeDefs.element import IElement


class IGenUnit(IElement):
    unitNumber: str
    installedCapacity: str
    mvaCapacity: str
    generatingVoltage: str
