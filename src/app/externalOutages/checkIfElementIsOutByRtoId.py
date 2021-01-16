import cx_Oracle


def checkIfElementIsOutByRtoId(pwcDbConnStr: str, elId: int, elTypeId: int, rtoId: int) -> bool:
    """check if a specified element is in out condition
    1. fetch the rto table entry for the given element id, element type and rto Id
    2. If there are no entries, then element is not out
    3. If there is an entry and the revivial date is null, then element is out, else element is not out
    Args:
        elId (int): [description]
        elTypeId (int): [description]
        rtoId (int): [description]

    Returns:
        bool: returns true if element is out
    """
    isElOut = False
    outageFetchSql = """
    SELECT
	rto.REVIVED_DATE 
    FROM
        REPORTING_WEB_UI_UAT.REAL_TIME_OUTAGE rto
    WHERE
        rto.ID = :rtoId
        AND rto.entity_id = :elTypeId
        AND rto.ELEMENT_ID = :elId
    """
    dbConn = None
    dbCur = None
    try:
        # get connection with raw data table
        dbConn = cx_Oracle.connect(pwcDbConnStr)

        # get cursor and execute fetch sql
        dbCur = dbConn.cursor()
        dbCur.execute(outageFetchSql, {
                      "rtoId": rtoId, "elId": elId, "elTypeId": elTypeId})

        colNames = [row[0] for row in dbCur.description]

        dbRows = dbCur.fetchall()
    except Exception as err:
        dbRows = []
        print('Error while fetching the outage of a element with elId = {0}, elTypeId = {1}, rtoId = {2} from pwc rto table'.format(
            elId, elTypeId, rtoId))
        print(err)
    finally:
        # closing database cursor and connection
        if dbCur is not None:
            dbCur.close()
        if dbConn is not None:
            dbConn.close()

    if not len(dbRows) == 0:
        revDate = dbRows[0][0]
        if revDate == None:
            isElOut = True

    return isElOut
