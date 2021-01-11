from src.typeDefs.element import IElement


class IBus(IElement):
    busNumber: str
    voltage: str
    substation: str
