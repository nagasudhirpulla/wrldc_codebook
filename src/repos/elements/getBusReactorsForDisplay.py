import cx_Oracle
from typing import List
from src.typeDefs.busReactor import IBusReactor


def getBusReactorsForDisplay(pwcDbConnStr: str) -> List[IBusReactor]:
    fetchSql = """SELECT
                    br.id as ELEMENT_ID,
                    br.REACTOR_NAME as ELEMENT_NAME,
                    br.MVAR_CAPACITY,
                    as2.SUBSTATION_NAME
                FROM
                    REPORTING_WEB_UI_UAT.BUS_REACTOR br
                LEFT JOIN REPORTING_WEB_UI_UAT.ASSOCIATE_SUBSTATION as2 ON
                    as2.ID = br.FK_SUBSTATION"""
    targetColumns = ['ELEMENT_ID', 'ELEMENT_NAME', 'MVAR_CAPACITY',
                     'SUBSTATION_NAME']
    elems: List[IBusReactor] = []
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
        print('Error while getting bus reactors for display')
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
        el: IBusReactor = {
            "elementId": row[colNames.index("ELEMENT_ID")],
            "elementName": row[colNames.index("ELEMENT_NAME")],
            "mvar": row[colNames.index("MVAR_CAPACITY")],
            "substation": row[colNames.index("SUBSTATION_NAME")],
        }
        elems.append(el)

    return elems
