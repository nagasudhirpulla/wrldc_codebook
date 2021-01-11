import cx_Oracle
from typing import List
from src.typeDefs.elemType import IElementType


def getElementTypes(pwcDbConnStr: str) -> List[IElementType]:
    fetchSql = """SELECT
                    em.ID,
                    em.ENTITY_NAME AS name
                FROM
                    REPORTING_WEB_UI_UAT.ENTITY_MASTER em
                WHERE
                    em.IS_OUTAGE_ENTITY = 1
                ORDER BY
                    em.ENTITY_NAME"""
    targetColumns = ['ID', 'NAME']
    elemTypes: List[IElementType] = []
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
        print('Error while getting element Types')
        print(err)
    finally:
        # closing database cursor and connection
        if dbCur is not None:
            dbCur.close()
        if dbConn is not None:
            dbConn.close()

    if (False in [(col in targetColumns) for col in colNames]):
        # all desired columns not fetched, hence return empty
        return elemTypes

    # fetch all rows
    for row in dbRows:
        elemType: IElementType = {
            "id": row[colNames.index("ID")],
            "name": row[colNames.index("NAME")]
        }
        elemTypes.append(elemType)

    return elemTypes
