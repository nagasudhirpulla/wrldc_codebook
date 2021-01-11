import cx_Oracle
from typing import List
from src.typeDefs.svc import ISvc


def getSvcsForDisplay(pwcDbConnStr: str) -> List[ISvc]:
    fetchSql = """SELECT
                    s.ID as ELEMENT_ID,
                    s.SVC_NAME as ELEMENT_NAME
                FROM
                    REPORTING_WEB_UI_UAT.SVC s"""
    targetColumns = ['ELEMENT_ID', 'ELEMENT_NAME']
    elems: List[ISvc] = []
    colNames = []
    dbRows = []
    dbConn = None
    dbCur = None
    try:
        # get connection with raw data table
        dbConn = cx_Oracle.connect(pwcDbConnStr)

        # get cursor and execute fetch sql
        dbCur = dbConn.cursor()
        dbCur.execute(fetchSql)

        colNames = [row[0] for row in dbCur.description]

        dbRows = dbCur.fetchall()
    except Exception as err:
        dbRows = []
        print('Error while getting hvdc poles for display')
        print(err)
    finally:
        # closing database cursor and connection
        if dbCur is not None:
            dbCur.close()
        if dbConn is not None:
            dbConn.close()

    if (False in [(col in targetColumns) for col in colNames]):
        # all desired columns not fetched, hence return empty
        return elems

    # fetch all rows
    for row in dbRows:
        el: ISvc = {
            "elementId": row[colNames.index("ELEMENT_ID")],
            "elementName": row[colNames.index("ELEMENT_NAME")]
        }
        elems.append(el)

    return elems
