import cx_Oracle
import datetime as dt


def deleteCode(appDbConnStr: str, codeId: int) -> bool:
    """delete a code with id

    Args:
        codeId (int): [description]
    Returns:
        bool: returns true if code is deleted successfully
    """
    dbConn = None
    dbCur = None
    isDeleteSuccess = True
    try:
        # get connection with application db
        dbConn = cx_Oracle.connect(appDbConnStr)
        # get cursor
        dbCur = dbConn.cursor()

        dbCur.execute(
            "update code_book.op_codes set is_deleted=1 where ID=:1", (codeId,))
        dbConn.commit()
    except Exception as err:
        isDeleteSuccess = False
        print('Error while deleted a code')
        print(err)
    finally:
        # closing database cursor and connection
        if dbCur is not None:
            dbCur.close()
        if dbConn is not None:
            dbConn.close()
    return isDeleteSuccess
