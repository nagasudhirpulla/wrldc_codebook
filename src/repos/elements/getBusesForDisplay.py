import cx_Oracle
from typing import List
from src.typeDefs.bus import IBus


def getBusesForDisplay(pwcDbConnStr: str) -> List[IBus]:
    fetchSql = """SELECT
                    b.id as ELEMENT_ID,
                    b.BUS_NAME as ELEMENT_NAME,
                    b.BUS_NUMBER,
                    vol.TRANS_ELEMENT_TYPE AS voltage,
                    as2.SUBSTATION_NAME
                FROM
                    REPORTING_WEB_UI_UAT.BUS b
                LEFT JOIN REPORTING_WEB_UI_UAT.ASSOCIATE_SUBSTATION as2 ON
                    as2.ID = b.FK_SUBSTATION_ID
                LEFT JOIN REPORTING_WEB_UI_UAT.TRANS_ELEMENT_TYPE_MASTER vol ON
                    vol.TRANS_ELEMENT_TYPE_ID = b.VOLTAGE"""
    targetColumns = ['ELEMENT_ID', 'ELEMENT_NAME', 'BUS_NUMBER', 'VOLTAGE',
                     'SUBSTATION_NAME']
    elems: List[IBus] = []
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
        print('Error while getting buses for display')
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
        el: IBus = {
            "elementId": row[colNames.index("ELEMENT_ID")],
            "elementName": row[colNames.index("ELEMENT_NAME")],
            "busNumber": row[colNames.index("BUS_NUMBER")],
            "substation": row[colNames.index("SUBSTATION_NAME")],
            "voltage": row[colNames.index("VOLTAGE")]
        }
        elems.append(el)

    return elems
