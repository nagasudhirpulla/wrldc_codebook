import datetime as dt
from typing import List, Optional
from src.repos.elements.getElementTypes import getElementTypes
from src.repos.elements.getBaysForDisplay import getBaysForDisplay
from src.typeDefs.bay import IBay


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
