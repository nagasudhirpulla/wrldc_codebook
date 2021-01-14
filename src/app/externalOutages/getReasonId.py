import cx_Oracle


def getReasonId(pwcDbConnStr: str, reason: str, outageTypeId: int) -> int:
    """get the reason id for a reason, create if required

    Args:
        pwcDbConnStr (str): [description]
        reason (str): [description]
        outageTypeId (int): [description]

    Returns:
        int: corresponding id of the reason in pwc database
    """
    fetchedReasonId = -1
    reasonIdFetchSql = """
    SELECT
        MAX(REAS.ID)
    FROM
        REPORTING_WEB_UI_UAT.OUTAGE_REASON REAS
    WHERE
        REAS.REASON = :1 AND OUTAGE_TYPE_ID = :2
    """
    dbConn = None
    dbCur = None
    try:
        # get connection with raw data table
        dbConn = cx_Oracle.connect(pwcDbConnStr)

        # get cursor and execute fetch sql
        dbCur = dbConn.cursor()
        dbCur.execute(reasonIdFetchSql, (reason, int(outageTypeId)))

        colNames = [row[0] for row in dbCur.description]

        # fetch all rows
        dbRows = dbCur.fetchall()
    except Exception as err:
        dbRows = []
        print('Error while fetching reason id by reason from pwc outage reason table')
        print(err)
    finally:
        # closing database cursor and connection
        if dbCur is not None:
            dbCur.close()
        if dbConn is not None:
            dbConn.close()
    if not len(dbRows) == 0:
        returnedId = dbRows[0][0]
        if not (returnedId == None):
            fetchedReasonId = returnedId
    if fetchedReasonId == -1:
        # reason not present, hence create one
        dbConn = None
        dbCur = None
        try:
            reasonInsertSql = """
            insert into REPORTING_WEB_UI_UAT.OUTAGE_REASON REAS(ID, REASON, OUTAGE_TYPE_ID)
            values (:1, :2, :3)
            """
            newReasIdFetchSql = """
            SELECT MAX(REAS.ID)+1 FROM REPORTING_WEB_UI_UAT.OUTAGE_REASON REAS
            """
            # get connection with raw data table
            dbConn = cx_Oracle.connect(pwcDbConnStr)
            # get cursor
            dbCur = dbConn.cursor()

            # max max reason id
            dbCur.execute(newReasIdFetchSql)
            dbRows = dbCur.fetchall()
            idVal = dbRows[0][0]

            # insert the new reason row
            dbCur.execute(reasonInsertSql, (idVal, reason, int(outageTypeId)))

            fetchedReasonId = idVal

            # commit the changes
            dbConn.commit()
        except Exception as err:
            fetchedReasonId = -1
            print('Error while creation of reason in pwc outage reason table')
            print(err)
        finally:
            # closing database cursor and connection
            if dbCur is not None:
                dbCur.close()
            if dbConn is not None:
                dbConn.close()
    return fetchedReasonId
