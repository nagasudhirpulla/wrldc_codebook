import datetime as dt
from typing import List, Optional
from src.repos.elements.getElementTypes import getElementTypes
from src.repos.elements.getBaysForDisplay import getBaysForDisplay
from src.repos.elements.getTransLineCktsForDisplay import getTranLineCktsForDisplay
from src.repos.elements.getBusesForDisplay import getBusesForDisplay
from src.repos.elements.getBusReactorsForDisplay import getBusReactorsForDisplay
from src.repos.elements.getFilterBanksForDisplay import getFilterBanksForDisplay
from src.repos.elements.getFscsForDisplay import getFscsForDisplay
from src.repos.elements.getGeneratingUnitsForDisplay import getGeneratingUnitsForDisplay
from src.repos.elements.getHvdcLineCktsForDisplay import getHvdcLineCktsForDisplay
from src.repos.elements.getHvdcPolesForDisplay import getHvdcPolesForDisplay
from src.repos.elements.getLineReactorsForDisplay import getLineReactorsForDisplay
from src.repos.elements.getSvcsForDisplay import getSvcsForDisplay
from src.repos.elements.getTcscsForDisplay import getTcscsForDisplay
from src.repos.elements.getTransformersForDisplay import getTransformersForDisplay
from src.typeDefs.bay import IBay
from src.typeDefs.transLineCkt import ITransLineCkt
from src.typeDefs.bus import IBus
from src.typeDefs.busReactor import IBusReactor
from src.typeDefs.filterBank import IFilterBank
from src.typeDefs.fsc import IFsc
from src.typeDefs.genUnit import IGenUnit
from src.typeDefs.hvdcLineCkt import IHvdcLineCkt
from src.typeDefs.hvdcPole import IHvdcPole
from src.typeDefs.lineReactor import ILineReactor
from src.typeDefs.svc import ISvc
from src.typeDefs.tcsc import ITcsc
from src.typeDefs.transformer import ITransformer


class ElementsRepo():
    """Repository class for Elements data of outage software
    """
    pwcDbConnStr: str = ""

    def __init__(self, dbConStr: str) -> None:
        """constructor method
        Args:
            dbConStr (str): database connection string to outage software
        """
        self.pwcDbConnStr = dbConStr

    def getElementTypes(self) -> List[str]:
        return getElementTypes(self.pwcDbConnStr)

    def getBaysForDisplay(self) -> List[IBay]:
        return getBaysForDisplay(self.pwcDbConnStr)

    def getTranLineCktsForDisplay(self) -> List[ITransLineCkt]:
        return getTranLineCktsForDisplay(self.pwcDbConnStr)

    def getBusesForDisplay(self) -> List[IBus]:
        return getBusesForDisplay(self.pwcDbConnStr)

    def getBusReactorsForDisplay(self) -> List[IBusReactor]:
        return getBusReactorsForDisplay(self.pwcDbConnStr)

    def getFilterBanksForDisplay(self) -> List[IFilterBank]:
        return getFilterBanksForDisplay(self.pwcDbConnStr)

    def getFscsForDisplay(self) -> List[IFsc]:
        return getFscsForDisplay(self.pwcDbConnStr)

    def getGeneratingUnitsForDisplay(self) -> List[IGenUnit]:
        return getGeneratingUnitsForDisplay(self.pwcDbConnStr)

    def getHvdcLineCktsForDisplay(self) -> List[IHvdcLineCkt]:
        return getHvdcLineCktsForDisplay(self.pwcDbConnStr)

    def getHvdcPolesForDisplay(self) -> List[IHvdcPole]:
        return getHvdcPolesForDisplay(self.pwcDbConnStr)

    def getLineReactorsForDisplay(self) -> List[ILineReactor]:
        return getLineReactorsForDisplay(self.pwcDbConnStr)

    def getSvcsForDisplay(self) -> List[ISvc]:
        return getSvcsForDisplay(self.pwcDbConnStr)

    def getTcscsForDisplay(self) -> List[ITcsc]:
        return getTcscsForDisplay(self.pwcDbConnStr)

    def getTransformersForDisplay(self) -> List[ITransformer]:
        return getTransformersForDisplay(self.pwcDbConnStr)
