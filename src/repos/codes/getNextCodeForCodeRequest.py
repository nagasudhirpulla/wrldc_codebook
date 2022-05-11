import cx_Oracle
import datetime as dt
from typing import List, Optional, Any
from src.app.utils.getNewCodePlaceHolder import getNewCodePlaceHolder
from src.typeDefs.code import ICode


def getNextCodeForCodeRequest(appDbConnStr: str) -> Optional[str]:
    """ gets the next auto code for creating a new code

    Args:
        dbCur (Any): db cursor through which data is to be fetched

    Returns:
        Optional[str]: auto generated code for inserting new code
    """
    latestIdFetchsql = """
            select code_str
            from code_book.op_codes 
            where created_at=(select max(created_at) from code_book.op_codes where is_deleted=0) 
            and is_deleted=0
            order by code_str desc
        """

    # initialise code object
    dbConn = None
    dbCur = None
    # get connection with raw data table
    dbConn = cx_Oracle.connect(appDbConnStr)
    # get cursor for raw data table
    dbCur = dbConn.cursor()
    colNames = []
    dbRows = []
    try:
        dbCur.execute(latestIdFetchsql)

        colNames = [row[0] for row in dbCur.description]

        # fetch all rows
        dbRows = dbCur.fetchall()
    except Exception as err:
        dbRows = []
        print('Error while fetching latest code str from app db')
        print(err)

    targetColumns = ["CODE_STR"]
    if (False in [(col in targetColumns) for col in colNames]):
        # all desired columns not fetched, hence return empty
        return None

    if len(dbRows) == 0:
        return None

    row = dbRows[0]

    # get the latest code str
    latestCodeStr: str = row[colNames.index('CODE_STR')]

    # split the code by '/'
    lastCodeSeg = latestCodeStr.split("/")[-1]

    # initialize new code integer as None
    newCodeInt = None

    # derive new code integer if possible
    try:
        latestCodeInt = int(lastCodeSeg)
        if latestCodeInt > 0:
            newCodeInt = latestCodeInt + 1
    except Exception as err:
        print('Error while parsing latest code for next code')
        print(err)

    # generate next code from latest code integer if possible
    nextCode: Optional[str] = getNewCodePlaceHolder()+str(newCodeInt) if not newCodeInt == None else None

    return nextCode
