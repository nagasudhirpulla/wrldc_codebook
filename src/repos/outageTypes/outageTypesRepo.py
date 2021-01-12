import cx_Oracle
import datetime as dt
from typing import List, Optional, TypedDict


class IOutageType(TypedDict):
    id: int
    name: str
    isGenerator: int


class OutageTypesRepo():
    """Repository class for outage types data of outage software
    """
    pwcDbConnStr: str = ""

    def __init__(self, dbConStr: str) -> None:
        """constructor method
        Args:
            dbConStr (str): database connection string to outage software
        """
        self.pwcDbConnStr = dbConStr

    def getRealTimeOutageTypes(self) -> List[IOutageType]:
        fetchSql = """SELECT
                        ID, NAME, IS_GENERATOR 
                    FROM
                        REPORTING_WEB_UI_UAT.SHUTDOWN_OUTAGE_TYPE SD_TYPE
                    WHERE
                        SD_TYPE.IS_APPROVED = 0"""
        targetColumns = ['ID', 'NAME', 'IS_GENERATOR']
        outageTypes: List[IOutageType] = []
        colNames = []
        dbRows = []
        dbConn = None
        dbCur = None
        try:
            # get connection with raw data table
            dbConn = cx_Oracle.connect(self.pwcDbConnStr)

            # get cursor and execute fetch sql
            dbCur = dbConn.cursor()
            dbCur.execute(fetchSql)

            colNames = [row[0] for row in dbCur.description]

            dbRows = dbCur.fetchall()
        except Exception as err:
            dbRows = []
            print('Error while getting real time outage Types')
            print(err)
        finally:
            # closing database cursor and connection
            if dbCur is not None:
                dbCur.close()
            if dbConn is not None:
                dbConn.close()

        if (False in [(col in targetColumns) for col in colNames]):
            # all desired columns not fetched, hence return empty
            return outageTypes

        # fetch all rows
        for row in dbRows:
            oType: IOutageType = {
                "id": row[colNames.index("ID")],
                "name": row[colNames.index("NAME")],
                "isGenerator": row[colNames.index("IS_GENERATOR")]
            }
            outageTypes.append(oType)

        return outageTypes
