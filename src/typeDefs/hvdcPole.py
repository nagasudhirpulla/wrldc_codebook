from src.typeDefs.element import IElement


class IHvdcPole(IElement):
    substation: str
    voltage: str
