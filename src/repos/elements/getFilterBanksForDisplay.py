import cx_Oracle
from typing import List
from src.typeDefs.filterBank import IFilterBank


def getFilterBanksForDisplay(pwcDbConnStr: str) -> List[IFilterBank]:
    fetchSql = """SELECT
                    fb.ID as ELEMENT_ID,
                    asb.SUBSTATION_NAME||' Filter bank - '||fb.FILTERBANK_NUMBER AS ELEMENT_NAME,
                    asb.SUBSTATION_NAME AS substation,
                    vol.TRANS_ELEMENT_TYPE AS voltage,
                    fb.MVAR,
                    fb.IS_SWITCHABLE,
                    fb.FILTERBANK_NUMBER
                FROM
                    REPORTING_WEB_UI_UAT.FILTER_BANK fb
                LEFT JOIN REPORTING_WEB_UI_UAT.ASSOCIATE_SUBSTATION asb ON
                    asb.id = fb.SUBSTATION_ID
                LEFT JOIN REPORTING_WEB_UI_UAT.TRANS_ELEMENT_TYPE_MASTER vol ON
                    vol.TRANS_ELEMENT_TYPE_ID = fb.VOLTAGE_ID"""
    targetColumns = ['ELEMENT_ID', 'ELEMENT_NAME', 'SUBSTATION',
                     'VOLTAGE', 'MVAR', 'IS_SWITCHABLE',
                     'FILTERBANK_NUMBER']
    elems: List[IFilterBank] = []
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
        print('Error while getting filter banks for display')
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
        el: IFilterBank = {
            "elementId": row[colNames.index("ELEMENT_ID")],
            "elementName": row[colNames.index("ELEMENT_NAME")],
            "substation": row[colNames.index("SUBSTATION")],
            "voltage": row[colNames.index("VOLTAGE")],
            "mvar": row[colNames.index("MVAR")],
            "isSwitchable": row[colNames.index("IS_SWITCHABLE")],
            "filterBankNumber": row[colNames.index("FILTERBANK_NUMBER")]
        }
        elems.append(el)

    return elems
