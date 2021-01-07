import cx_Oracle
import datetime as dt
from src.repos.codes.insertGenericCode import insertGenericCode
from src.repos.codes.getCodesBetweenDates import getCodesBetweenDates
from typing import List
from src.typeDefs.code import ICode


class CodesRepo():
    """Repository class for Codes data of application
    """
    appDbConnStr: str = ""

    def __init__(self, dbConStr: str) -> None:
        """constructor method
        Args:
            dbConStr (str): database connection string
        """
        self.appDbConnStr = dbConStr

    def insertGenericCode(self, code_issue_time: dt.datetime,
                          code_str: str, other_ldc_codes: str,
                          code_description: str, code_execution_time: dt.datetime,
                          code_tags: str, code_issued_by: str, code_issued_to: str) -> bool:
        """inserts a generic code into the app db
        Returns:
            bool: returns true if process is ok
        """
        isInsertSuccess = insertGenericCode(self.appDbConnStr, code_issue_time,
                                            code_str, other_ldc_codes,
                                            code_description, code_execution_time,
                                            code_tags, code_issued_by, code_issued_to)
        return isInsertSuccess

    def getCodesBetweenDates(self, startDt: dt.datetime, endDt: dt.datetime) -> List[ICode]:
        """fetches codes between 2 dates from app db

        Args:
            startDt (dt.datetime): [description]
            endDt (dt.datetime): [description]

        Returns:
            List[ICode]: list of code objects
        """
        return getCodesBetweenDates(self.appDbConnStr, startDt, endDt)
