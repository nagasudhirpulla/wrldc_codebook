from typing import Optional
import cx_Oracle
import datetime as dt


def getExpectedRevivalTime(pwcDbConnStr: str, sdReqId: int) -> Optional[dt.datetime]:
    fetchSql = """
    SELECT
        SD.APPROVED_END_DATE
    FROM
        REPORTING_WEB_UI_UAT.SHUTDOWN sd
    WHERE
        SHUTDOWN_REQUEST_ID = :1
    """
    targetColumns = ['APPROVED_END_DATE']
    expectedRevivalDt: Optional[dt.datetime] = None
    colNames = []
    dbRows = []
    dbConn = None
    dbCur = None
    try:
        # get connection with raw data table
        dbConn = cx_Oracle.connect(pwcDbConnStr)

        # get cursor and execute fetch sql
        dbCur = dbConn.cursor()
        dbCur.execute(fetchSql, (sdReqId,))

        colNames = [row[0] for row in dbCur.description]

        dbRows = dbCur.fetchall()
    except Exception as err:
        dbRows = []
        print('Error while getting approved end date for approved shutdown from pwc db')
        print(err)
    finally:
        # closing database cursor and connection
        if dbCur is not None:
            dbCur.close()
        if dbConn is not None:
            dbConn.close()

    if (False in [(col in targetColumns) for col in colNames]):
        # all desired columns not fetched, hence return empty
        return expectedRevivalDt

    if len(dbRows) > 0:
        expectedRevivalDt = dbRows[0][colNames.index("APPROVED_END_DATE")]

    return expectedRevivalDt
