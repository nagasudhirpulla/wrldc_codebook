import cx_Oracle
from typing import List
from src.typeDefs.genUnit import IGenUnit


def getGeneratingUnitsForDisplay(pwcDbConnStr: str) -> List[IGenUnit]:
    fetchSql = """SELECT
                    gu.id as ELEMENT_ID,
                    gu.UNIT_NAME as ELEMENT_NAME,
                    gu.UNIT_NUMBER,
                    gu.INSTALLED_CAPACITY,
                    gu.MVA_CAPACITY, 
                    vol.TRANS_ELEMENT_TYPE AS GENERATING_VOLTAGE
                FROM
                    REPORTING_WEB_UI_UAT.GENERATING_UNIT gu
                LEFT JOIN REPORTING_WEB_UI_UAT.TRANS_ELEMENT_TYPE_MASTER vol ON
                    vol.TRANS_ELEMENT_TYPE_ID = gu.GENERATING_VOLTAGE_KV
                WHERE gu.ACTIVE=1"""
    targetColumns = ['ELEMENT_ID', 'ELEMENT_NAME', 'UNIT_NUMBER',
                     'INSTALLED_CAPACITY', 'MVA_CAPACITY', 'GENERATING_VOLTAGE']
    elems: List[IGenUnit] = []
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
        print('Error while getting generating units for display')
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
        el: IGenUnit = {
            "elementId": row[colNames.index("ELEMENT_ID")],
            "elementName": row[colNames.index("ELEMENT_NAME")],
            "unitNumber": row[colNames.index("UNIT_NUMBER")],
            "installedCapacity": row[colNames.index("INSTALLED_CAPACITY")],
            "mvaCapacity": row[colNames.index("MVA_CAPACITY")],
            "generatingVoltage": row[colNames.index("GENERATING_VOLTAGE")]
        }
        elems.append(el)

    return elems
