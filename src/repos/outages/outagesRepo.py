from src.typeDefs.unRevOutage import IUnRevOutage
from src.repos.outages.getLatestUnrevOutages import getLatestUnrevOutages
from typing import List
import cx_Oracle


class OutagesRepo():
    """Repository class for outages data of outage software
    """
    pwcDbConnStr: str = ""

    def __init__(self, dbConStr: str) -> None:
        """constructor method
        Args:
            dbConStr (str): database connection string to outage software
        """
        self.pwcDbConnStr = dbConStr

    def getLatestUnrevOutages(self) -> List[IUnRevOutage]:
        return getLatestUnrevOutages(self.pwcDbConnStr)
