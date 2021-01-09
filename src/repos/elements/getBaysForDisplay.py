import cx_Oracle
from typing import List
from src.typeDefs.bay import IBay


def getBaysForDisplay(pwcDbConnStr: str) -> List[IBay]:
    fetchSql = """SELECT
                    b.id,
                    b.BAY_NAME as name,
                    b.BAY_NUMBER ,
                    as2.SUBSTATION_NAME,
                    bt.type,
                    vol.TRANS_ELEMENT_TYPE AS voltage
                FROM
                    REPORTING_WEB_UI_UAT.BAY b
                LEFT JOIN REPORTING_WEB_UI_UAT.BAY_TYPE bt ON
                    bt.ID = b.BAY_TYPE_ID
                LEFT JOIN REPORTING_WEB_UI_UAT.ASSOCIATE_SUBSTATION as2 ON
                    as2.ID = b.STATION_ID
                LEFT JOIN REPORTING_WEB_UI_UAT.TRANS_ELEMENT_TYPE_MASTER vol ON
                    vol.TRANS_ELEMENT_TYPE_ID = b.VOLTAGE_ID"""
    targetColumns = ['ID', 'NAME', 'BAY_NUMBER', 'SUBSTATION_NAME',
                     'TYPE', 'VOLTAGE']
    bays: List[IBay] = []
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
        return bays

    # fetch all rows
    for row in dbRows:
        bay: IBay = {
            "id": row[colNames.index("ID")],
            "name": row[colNames.index("NAME")],
            "bayNumber": row[colNames.index("BAY_NUMBER")],
            "stationName": row[colNames.index("SUBSTATION_NAME")],
            "bayType": row[colNames.index("TYPE")],
            "voltage": row[colNames.index("VOLTAGE")]
        }
        bays.append(bay)

    return bays
