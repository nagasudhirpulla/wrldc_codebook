import cx_Oracle
from typing import Optional


def insertCodeTag(appDbConnStr: str, codeTag: str) -> bool:
    """inserts a code tag into the app db
    Returns:
        bool: returns true if process is ok
    """
    dbConn = None
    dbCur = None
    isInsertSuccess = True
    try:
        # get connection with raw data table
        dbConn = cx_Oracle.connect(appDbConnStr)
        # column names of the table
        colNames = ["TAG_NAME"]
        # get cursor for code tags table
        dbCur = dbConn.cursor()

        sqlVals = [codeTag]

        # text for sql place holders
        sqlPlaceHldrsTxt = ','.join([':{0}'.format(x+1)
                                     for x in range(len(colNames))])

        # insert the code tag
        codeTagInsSql = 'insert into code_book.code_tags({0}) values ({1})'.format(
            ','.join(colNames), sqlPlaceHldrsTxt)

        dbCur.execute(codeTagInsSql, sqlVals)

        # commit the changes
        dbConn.commit()
    except Exception as err:
        isInsertSuccess = False
        print('Error while creation of code tag')
        print(err)
    finally:
        # closing database cursor and connection
        if dbCur is not None:
            dbCur.close()
        if dbConn is not None:
            dbConn.close()
    return isInsertSuccess
