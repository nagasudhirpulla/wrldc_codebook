import cx_Oracle


def deleteCodeTag(appDbConnStr: str, codeTagId: int) -> bool:
    """delete a code tag with id
    Args:
        codeTagId (int): [description]
    Returns:
        bool: returns true if code tag is deleted successfully
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
            "delete from code_book.code_tags where ID=:1", (codeTagId,))
        dbConn.commit()
    except Exception as err:
        isDeleteSuccess = False
        print('Error while deleting a code tag')
        print(err)
    finally:
        # closing database cursor and connection
        if dbCur is not None:
            dbCur.close()
        if dbConn is not None:
            dbConn.close()
    return isDeleteSuccess
