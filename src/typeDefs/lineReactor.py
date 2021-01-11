from src.typeDefs.element import IElement


class ILineReactor(IElement):
    mvar: str
    substation: str
    lineName: str
