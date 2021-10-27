import cx_Oracle
import datetime as dt
from typing import List, Dict
from src.typeDefs.code import ICode


def getAllCodeTags(appDbConnStr: str) -> List[str]:
    """fetches all code tags from database
    Args:
        appDbConnStr (str): app db connection string

    Returns:
        List[ICode]: list of code objects
    """
    targetColumns = ['ID', 'TAG_NAME']
    codesFetchSql = """
            SELECT
                {0}
            FROM
                code_book.code_tags ct
            ORDER BY
                ct.TAG_NAME
        """.format(','.join(targetColumns))

    colNames = []
    dbRows = []
    dbConn = None
    dbCur = None
    try:
        # get connection with raw data table
        dbConn = cx_Oracle.connect(appDbConnStr)

        # get cursor and execute fetch sql
        dbCur = dbConn.cursor()
        dbCur.execute(codesFetchSql)

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
        return []

    # iterate through each row to populate result
    codeTags: List[str] = []
    for row in dbRows:
        tagName: str = row[colNames.index('TAG_NAME')]
        codeTags.append(tagName)
    return codeTags
