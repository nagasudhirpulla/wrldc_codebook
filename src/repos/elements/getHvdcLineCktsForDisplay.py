import cx_Oracle
from typing import List
from src.typeDefs.hvdcLineCkt import IHvdcLineCkt


def getHvdcLineCktsForDisplay(pwcDbConnStr: str) -> List[IHvdcLineCkt]:
    fetchSql = """SELECT
                    hlc.id as ELEMENT_ID,
                    hlc.LINE_CIRCUIT_NAME as ELEMENT_NAME,
                    hlc.CIRCUIT_NO,
                    line.voltage
                FROM
                    REPORTING_WEB_UI_UAT.HVDC_LINE_CIRCUIT hlc
                LEFT JOIN (
                    SELECT
                        hlm.*, vol.TRANS_ELEMENT_TYPE AS voltage
                    FROM
                        REPORTING_WEB_UI_UAT.HVDC_LINE_MASTER hlm
                    LEFT JOIN REPORTING_WEB_UI_UAT.TRANS_ELEMENT_TYPE_MASTER vol ON
                        vol.TRANS_ELEMENT_TYPE_ID = hlm.FROM_VOLTAGE) line ON
                    line.ID = HLC.HVDC_LINE_ID"""
    targetColumns = ['ELEMENT_ID', 'ELEMENT_NAME', 'CIRCUIT_NO',
                     'VOLTAGE']
    elems: List[IHvdcLineCkt] = []
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
        print('Error while getting hvdc line ckts for display')
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
        el: IHvdcLineCkt = {
            "elementId": row[colNames.index("ELEMENT_ID")],
            "elementName": row[colNames.index("ELEMENT_NAME")],
            "lineNumber": row[colNames.index("CIRCUIT_NO")],
            "voltage": row[colNames.index("VOLTAGE")]
        }
        elems.append(el)

    return elems
