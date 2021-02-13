import cx_Oracle
import datetime as dt
from typing import List, Dict
from src.typeDefs.code import ICode


def getCodesForRtoIds(appDbConnStr: str, rtoIds: List[int]) -> Dict[int, str]:
    """fetches codes corresponding to pwc RTO ids
    Args:
        appDbConnStr (str): app db connection string
        rtoIds (List[int]): List of pwc rto ids

    Returns:
        List[ICode]: list of code objects
    """
    if len(rtoIds) == 0:
        return {}
    targetColumns = ['CODES', 'PWC_RTO_ID']
    queryPlaceHolders = [':{0}'.format(i+1) for i, _ in enumerate(rtoIds)]
    codesFetchSql = """
            SELECT
                listagg(oc.CODE_STR, ', ' ) within group (order by oc.CODE_STR) AS CODES,
                oc.PWC_RTO_ID
            FROM
                code_book.op_codes oc
            WHERE
                oc.is_deleted = 0
                AND oc.PWC_RTO_ID IS NOT NULL
                AND oc.PWC_RTO_ID IN ({0})
            GROUP BY
                oc.PWC_RTO_ID
        """.format(','.join(queryPlaceHolders))

    colNames = []
    dbRows = []
    dbConn = None
    dbCur = None
    try:
        # get connection with raw data table
        dbConn = cx_Oracle.connect(appDbConnStr)

        # get cursor and execute fetch sql
        dbCur = dbConn.cursor()
        dbCur.execute(codesFetchSql, rtoIds)

        colNames = [row[0] for row in dbCur.description]

        # fetch all rows
        dbRows = dbCur.fetchall()
    except Exception as err:
        dbRows = []
        print('Error while fetching codes for RTO Ids')
        print(err)
    finally:
        # closing database cursor and connection
        if dbCur is not None:
            dbCur.close()
        if dbConn is not None:
            dbConn.close()

    if (False in [(col in targetColumns) for col in colNames]):
        # all desired columns not fetched, hence return empty
        return {}

    # iterate through each row to populate result
    rtoCodes: Dict[int, str] = {}
    for row in dbRows:
        rtoId: int = row[colNames.index('PWC_RTO_ID')]
        codes: str = row[colNames.index('CODES')]
        rtoCodes[rtoId] = codes
    return rtoCodes
