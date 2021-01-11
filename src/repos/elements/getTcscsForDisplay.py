import cx_Oracle
from typing import List
from src.typeDefs.tcsc import ITcsc


def getTcscsForDisplay(pwcDbConnStr: str) -> List[ITcsc]:
    fetchSql = """SELECT
                    t.ID as ELEMENT_ID,
                    t.TCSC_NAME as ELEMENT_NAME,
                    t.PERC_VARIABLE_COMPENSATION,
                    t.PERC_FIXED_COMPENSATION
                FROM
                    REPORTING_WEB_UI_UAT.TCSC t"""
    targetColumns = ['ELEMENT_ID', 'ELEMENT_NAME',
                     'PERC_VARIABLE_COMPENSATION', 'PERC_FIXED_COMPENSATION']
    elems: List[ITcsc] = []
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
        el: ITcsc = {
            "elementId": row[colNames.index("ELEMENT_ID")],
            "elementName": row[colNames.index("ELEMENT_NAME")],
            "variableCompensationPerc": row[colNames.index("PERC_VARIABLE_COMPENSATION")],
            "fixedCompensationPerc": row[colNames.index("PERC_FIXED_COMPENSATION")]
        }
        elems.append(el)

    return elems
