import cx_Oracle
from typing import List
from src.typeDefs.transLineCkt import ITransLineCkt


def getTranLineCktsForDisplay(pwcDbConnStr: str) -> List[ITransLineCkt]:
    fetchSql = """SELECT
                    ckt.id as element_id,
                    ckt.LINE_CIRCUIT_NAME as element_name,
                    ckt.CIRCUIT_NUMBER,
                    ckt.LENGTH,
                    line.voltage
                FROM
                    REPORTING_WEB_UI_UAT.AC_TRANSMISSION_LINE_CIRCUIT ckt
                LEFT JOIN (
                    SELECT
                        lm.*, vol.TRANS_ELEMENT_TYPE AS voltage
                    FROM
                        REPORTING_WEB_UI_UAT.AC_TRANS_LINE_MASTER lm
                    LEFT JOIN REPORTING_WEB_UI_UAT.TRANS_ELEMENT_TYPE_MASTER vol ON
                        vol.TRANS_ELEMENT_TYPE_ID = lm.VOLTAGE_LEVEL ) line ON
                    line.id = ckt.line_id"""
    targetColumns = ['ELEMENT_ID', 'ELEMENT_NAME', 'CIRCUIT_NUMBER', 'LENGTH',
                     'VOLTAGE']
    lines: List[ITransLineCkt] = []
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
        print('Error while getting bays for display')
        print(err)
    finally:
        # closing database cursor and connection
        if dbCur is not None:
            dbCur.close()
        if dbConn is not None:
            dbConn.close()

    if (False in [(col in targetColumns) for col in colNames]):
        # all desired columns not fetched, hence return empty
        return lines

    # fetch all rows
    for row in dbRows:
        line: ITransLineCkt = {
            "elementId": row[colNames.index("ELEMENT_ID")],
            "elementName": row[colNames.index("ELEMENT_NAME")],
            "cktNumber": row[colNames.index("CIRCUIT_NUMBER")],
            "length": row[colNames.index("LENGTH")],
            "voltage": row[colNames.index("VOLTAGE")]
        }
        lines.append(line)

    return lines
