import cx_Oracle
from typing import List
from src.typeDefs.fsc import IFsc


def getFscsForDisplay(pwcDbConnStr: str) -> List[IFsc]:
    fetchSql = """SELECT
                    f.ID as ELEMENT_ID,
                    f.FSC_NAME as ELEMENT_NAME,
                    as2.SUBSTATION_NAME
                FROM
                    REPORTING_WEB_UI_UAT.FSC f
                LEFT JOIN REPORTING_WEB_UI_UAT.ASSOCIATE_SUBSTATION as2 ON
                    as2.ID = f.FK_SUBSTATION"""
    targetColumns = ['ELEMENT_ID', 'ELEMENT_NAME', 'SUBSTATION_NAME']
    elems: List[IFsc] = []
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
        print('Error while getting fscs for display')
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
        el: IFsc = {
            "elementId": row[colNames.index("ELEMENT_ID")],
            "elementName": row[colNames.index("ELEMENT_NAME")],
            "substation": row[colNames.index("SUBSTATION_NAME")]
        }
        elems.append(el)

    return elems
