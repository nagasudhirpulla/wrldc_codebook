import cx_Oracle


def checkIfElementIsOut(pwcDbConnStr: str, elId: int, elTypeId: int) -> bool:
    """check if a specified element is in out condition
    1. fetch the latest rto table entry for the given element id and element type
    2. If there are no entries, then element is not out
    3. If there is an entry and the revivial date is null, then element is out, else element is not out
    Args:
        elId (int): [description]
        elTypeId (int): [description]

    Returns:
        bool: returns true if element is out
    """
    isElOut = False
    latestOutageFetchSql = """
    SELECT
	rto.REVIVED_DATE 
    FROM
        REPORTING_WEB_UI_UAT.REAL_TIME_OUTAGE rto
    WHERE
        to_char(rto.OUTAGE_DATE , 'YYYY-MM-DD')|| ' ' || rto.OUTAGE_TIME = (
        SELECT
            MAX(to_char(OUTAGE_DATE , 'YYYY-MM-DD')|| ' ' || OUTAGE_TIME) AS out_date_time
        FROM
            reporting_web_ui_uat.REAL_TIME_OUTAGE
        WHERE
            entity_id = :elTypeId
            AND ELEMENT_ID = :elId)
        AND rto.entity_id = :elTypeId
        AND rto.ELEMENT_ID = :elId
    ORDER BY rto.OUTAGE_DATE DESC, OUTAGE_TIME DESC, rto.ID DESC 
    """
    dbConn = None
    dbCur = None
    try:
        # get connection with raw data table
        dbConn = cx_Oracle.connect(pwcDbConnStr)

        # get cursor and execute fetch sql
        dbCur = dbConn.cursor()
        dbCur.execute(latestOutageFetchSql, {
                      "elId": elId, "elTypeId": elTypeId})

        colNames = [row[0] for row in dbCur.description]

        dbRows = dbCur.fetchall()
    except Exception as err:
        dbRows = []
        print('Error while fetching the latest outage of a element with elId = {0}, elTypeId = {1} from pwc rto table'.format(
            elId, elTypeId))
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
