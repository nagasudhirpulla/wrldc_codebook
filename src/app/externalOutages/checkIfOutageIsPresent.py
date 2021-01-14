import cx_Oracle


def checkIfOutageIsPresent(pwcDbConnStr: str, rtoId: int) -> bool:
    """check if outage is present in pwc db

    Args:
        pwcDbConnStr (str): [description]
        rtoId (int): [description]

    Returns:
        bool: True if outage is present in pwc db
    """
    outageCount = 0
    countFetchSql = """
    SELECT
	count(*)
    FROM
        REPORTING_WEB_UI_UAT.REAL_TIME_OUTAGE RTO
    WHERE
        RTO.ID = :1
    """
    dbConn = None
    dbCur = None
    try:
        # get connection with raw data table
        dbConn = cx_Oracle.connect(pwcDbConnStr)

        # get cursor and execute fetch sql
        dbCur = dbConn.cursor()
        dbCur.execute(countFetchSql, (rtoId,))

        colNames = [row[0] for row in dbCur.description]

        dbRows = dbCur.fetchall()
    except Exception as err:
        dbRows = []
        print('Error while fetching the count of rows by id from pwc rto table')
        print(err)
    finally:
        # closing database cursor and connection
        if dbCur is not None:
            dbCur.close()
        if dbConn is not None:
            dbConn.close()

    if not len(dbRows) == 0:
        outageCount = dbRows[0][0]

    return True if outageCount > 0 else False
