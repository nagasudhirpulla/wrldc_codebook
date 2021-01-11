import cx_Oracle
from typing import List
from src.typeDefs.lineReactor import ILineReactor


def getLineReactorsForDisplay(pwcDbConnStr: str) -> List[ILineReactor]:
    fetchSql = """SELECT
                    lr.id as ELEMENT_ID,
                    lr.REACTOR_NAME as ELEMENT_NAME,
                    lr.MVAR_CAPACITY,
                    as2.SUBSTATION_NAME,
                    ATLC.LINE_CIRCUIT_NAME
                FROM
                    REPORTING_WEB_UI_UAT.LINE_REACTOR lr
                LEFT JOIN REPORTING_WEB_UI_UAT.ASSOCIATE_SUBSTATION as2 ON
                    as2.ID = lr.FK_SUBSTATION
                LEFT JOIN REPORTING_WEB_UI_UAT.AC_TRANSMISSION_LINE_CIRCUIT atlc ON
                    ATLC.id = lr.FK_LINE_ID"""
    targetColumns = ['ELEMENT_ID', 'ELEMENT_NAME', 'MVAR_CAPACITY',
                     'SUBSTATION_NAME', 'LINE_CIRCUIT_NAME']
    elems: List[ILineReactor] = []
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
        el: ILineReactor = {
            "elementId": row[colNames.index("ELEMENT_ID")],
            "elementName": row[colNames.index("ELEMENT_NAME")],
            "mvar": row[colNames.index("MVAR_CAPACITY")],
            "substation": row[colNames.index("SUBSTATION_NAME")],
            "lineName": row[colNames.index("LINE_CIRCUIT_NAME")]
        }
        elems.append(el)

    return elems
