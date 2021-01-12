import cx_Oracle
import datetime as dt
from typing import List, Optional, TypedDict


class IOutageTag(TypedDict):
    id: int
    name: str
    outageTypeId: int


class OutageTagsRepo():
    """Repository class for outage tags data of outage software
    """
    pwcDbConnStr: str = ""

    def __init__(self, dbConStr: str) -> None:
        """constructor method
        Args:
            dbConStr (str): database connection string to outage software
        """
        self.pwcDbConnStr = dbConStr

    def getRealTimeOutageTags(self) -> List[IOutageTag]:
        fetchSql = """SELECT
                        SD_TAG.ID,
                        SD_TAG.NAME,
                        SD_TAG.SHUTDOWN_OUTAGE_TYPE_ID
                    FROM
                        REPORTING_WEB_UI_UAT.SHUTDOWN_OUTAGE_TAG SD_TAG
                    LEFT JOIN REPORTING_WEB_UI_UAT.SHUTDOWN_OUTAGE_TYPE SD_TYPE ON
                        SD_TYPE.ID = SD_TAG.SHUTDOWN_OUTAGE_TYPE_ID
                    WHERE
                        SD_TYPE.IS_APPROVED = 0"""
        targetColumns = ['ID', 'NAME', 'SHUTDOWN_OUTAGE_TYPE_ID']
        outageTags: List[IOutageTag] = []
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
            print('Error while getting real time outage Tags')
            print(err)
        finally:
            # closing database cursor and connection
            if dbCur is not None:
                dbCur.close()
            if dbConn is not None:
                dbConn.close()

        if (False in [(col in targetColumns) for col in colNames]):
            # all desired columns not fetched, hence return empty
            return outageTags

        # fetch all rows
        for row in dbRows:
            oTag: IOutageTag = {
                "id": row[colNames.index("ID")],
                "name": row[colNames.index("NAME")],
                "outageTypeId": row[colNames.index("SHUTDOWN_OUTAGE_TYPE_ID")]
            }
            outageTags.append(oTag)

        return outageTags
