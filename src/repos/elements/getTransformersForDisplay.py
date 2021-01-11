import cx_Oracle
from typing import List
from src.typeDefs.transformer import ITransformer


def getTransformersForDisplay(pwcDbConnStr: str) -> List[ITransformer]:
    fetchSql = """SELECT
                    t.id as ELEMENT_ID, 
                    t.TRANSFORMER_NAME as ELEMENT_NAME,
                    t.MVA_CAPACITY,
                    t.TYPE_GT_ICT
                FROM
                    REPORTING_WEB_UI_UAT.TRANSFORMER t"""
    targetColumns = ['ELEMENT_ID', 'ELEMENT_NAME',
                     'MVA_CAPACITY', 'TYPE_GT_ICT']
    elems: List[ITransformer] = []
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
        el: ITransformer = {
            "elementId": row[colNames.index("ELEMENT_ID")],
            "elementName": row[colNames.index("ELEMENT_NAME")],
            "mvaCapacity": row[colNames.index("MVA_CAPACITY")],
            "transformerType": row[colNames.index("TYPE_GT_ICT")]
        }
        elems.append(el)

    return elems
