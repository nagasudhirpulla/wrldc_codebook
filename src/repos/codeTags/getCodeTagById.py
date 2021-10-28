import cx_Oracle
from typing import Optional
from src.typeDefs.codeTag import ICodeTag


def getCodeTagById(appDbConnStr: str, codeTagId: int) -> Optional[ICodeTag]:
    """fetches code tag by id

    Args:
        appDbConnStr (str): app db connection string
        codeTagId (int): [description]

    Returns:
        Optional[ICode]: code tag object
    """
    targetColumns = ['ID', 'TAG_NAME']

    codeTagsFetchSql = """
            select {0}
            from code_book.code_tags 
            where id=:1
        """.format(','.join(targetColumns))

    # initialise code tag object
    codeTag: Optional[ICodeTag] = None
    colNames = []
    dbRows = []
    dbConn = None
    dbCur = None
    try:
        # get connection with raw data table
        dbConn = cx_Oracle.connect(appDbConnStr)

        # get cursor and execute fetch sql
        dbCur = dbConn.cursor()
        dbCur.execute(codeTagsFetchSql, (codeTagId,))

        colNames = [row[0] for row in dbCur.description]

        # fetch all rows
        dbRows = dbCur.fetchall()
    except Exception as err:
        dbRows = []
        print('Error while creation of fetching code tag by Id')
        print(err)
    finally:
        # closing database cursor and connection
        if dbCur is not None:
            dbCur.close()
        if dbConn is not None:
            dbConn.close()

    if (False in [(col in targetColumns) for col in colNames]):
        # all desired columns not fetched, hence return empty
        return None

    if len(dbRows) == 0:
        return codeTag

    row = dbRows[0]
    id: ICodeTag["id"] = row[colNames.index('ID')]
    codeTagName: ICodeTag["tag"] = row[colNames.index('TAG_NAME')]
    codeTag = {
        "id": id,
        "tag": codeTagName
    }
    return codeTag
