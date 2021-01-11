import cx_Oracle
from typing import List
from src.typeDefs.hvdcPole import IHvdcPole


def getHvdcPolesForDisplay(pwcDbConnStr: str) -> List[IHvdcPole]:
    fetchSql = """SELECT
                    hp.id as ELEMENT_ID,
                    hp.POLE_NAME as ELEMENT_NAME,
                    stn.SUBSTATION_NAME,
                    stn.voltage
                FROM
                    REPORTING_WEB_UI_UAT.HVDC_POLE hp
                LEFT JOIN (
                    SELECT
                        as2.*, vol.TRANS_ELEMENT_TYPE AS voltage
                    FROM
                        REPORTING_WEB_UI_UAT.ASSOCIATE_SUBSTATION as2
                    LEFT JOIN REPORTING_WEB_UI_UAT.TRANS_ELEMENT_TYPE_MASTER vol ON
                        vol.TRANS_ELEMENT_TYPE_ID = as2.VOLTAGE_LEVEL) stn ON
                    stn.id = hp.FK_SUBSTATION"""
    targetColumns = ['ELEMENT_ID', 'ELEMENT_NAME', 'SUBSTATION_NAME',
                     'VOLTAGE']
    elems: List[IHvdcPole] = []
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
        el: IHvdcPole = {
            "elementId": row[colNames.index("ELEMENT_ID")],
            "elementName": row[colNames.index("ELEMENT_NAME")],
            "substation": row[colNames.index("SUBSTATION_NAME")],
            "voltage": row[colNames.index("VOLTAGE")]
        }
        elems.append(el)

    return elems
