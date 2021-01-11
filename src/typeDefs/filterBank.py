from src.typeDefs.element import IElement


class IFilterBank(IElement):
    substation: str
    voltage: str
    mvar: str
    isSwitchable: str
    filterBankNumber: str
