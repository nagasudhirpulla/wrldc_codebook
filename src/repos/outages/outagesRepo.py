from src.typeDefs.unRevOutage import IUnRevOutage
from src.typeDefs.approvedOutage import IApprovedOutage
from src.repos.outages.getLatestUnrevOutages import getLatestUnrevOutages
from src.repos.outages.getApprovedOutages import getApprovedOutages
from typing import List
import datetime as dt


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

    def getApprovedOutages(self, targetDt: dt.datetime) -> List[IApprovedOutage]:
        return getApprovedOutages(self.pwcDbConnStr, targetDt)
