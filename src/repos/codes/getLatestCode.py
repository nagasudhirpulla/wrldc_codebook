import cx_Oracle
import datetime as dt
from typing import List, Optional
from src.typeDefs.code import ICode
from src.repos.codes.getCodeById import getCodeById


def getLatestCode(appDbConnStr: str) -> Optional[ICode]:
    """get latest created code from db

    Args:
        appDbConnStr (str): app db connection string

    Returns:
        Optional[ICode]: code object
    """
    latestIdFetchsql = """
            select id
            from code_book.op_codes 
            where code_issue_time=(select max(code_issue_time) from code_book.op_codes where is_deleted=0) 
            and is_deleted=0
            order by id desc
        """

    # initialise code object
    code: Optional[ICode] = None
    colNames = []
    dbRows = []
    dbConn = None
    dbCur = None
    try:
        # get connection with raw data table
        dbConn = cx_Oracle.connect(appDbConnStr)

        # get cursor and execute fetch sql
        dbCur = dbConn.cursor()
        dbCur.execute(latestIdFetchsql)

        colNames = [row[0] for row in dbCur.description]

        # fetch all rows
        dbRows = dbCur.fetchall()
    except Exception as err:
        dbRows = []
        print('Error while fetching latest code id from app db')
        print(err)
    finally:
        # closing database cursor and connection
        if dbCur is not None:
            dbCur.close()
        if dbConn is not None:
            dbConn.close()

    targetColumns = ["ID"]
    if (False in [(col in targetColumns) for col in colNames]):
        # all desired columns not fetched, hence return empty
        return None

    if len(dbRows) == 0:
        return None

    row = dbRows[0]
    latestCodeId: ICode["id"] = row[colNames.index('ID')]
    # get latest code by id
    code = getCodeById(appDbConnStr=appDbConnStr, codeId=latestCodeId)
    return code
