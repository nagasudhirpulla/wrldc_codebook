import cx_Oracle
from typing import List
from src.typeDefs.codeTag import ICodeTag


def getAllCodeTags(appDbConnStr: str) -> List[ICodeTag]:
    """fetches all code tags from database
    Args:
        appDbConnStr (str): app db connection string

    Returns:
        List[ICodeTag]: list of code tag objects
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
    codeTags: List[ICodeTag] = []
    for row in dbRows:
        id: int = row[colNames.index('ID')]
        tagName: str = row[colNames.index('TAG_NAME')]
        codeTagObj: ICodeTag = {
            "id": id,
            "tag": tagName
        }
        codeTags.append(codeTagObj)
    return codeTags
