import cx_Oracle
import datetime as dt
from typing import Optional, Union


def insertElementCode(appDbConnStr: str, code_issue_time: Optional[dt.datetime],
                      code_str: str, other_ldc_codes: str,
                      code_description: str, code_execution_time: dt.datetime,
                      code_tags: str, code_issued_by: str, code_issued_to: str,
                      pwc_element_type_id: int, pwc_element_id: int,
                      pwc_element_name: str, pwc_element_type: str) -> bool:
    """inserts an element code into the app db
    Returns:
        bool: returns true if process is ok
    """
    dbConn = None
    dbCur = None
    isInsertSuccess = True
    try:
        # get connection with raw data table
        dbConn = cx_Oracle.connect(appDbConnStr)
        # column names of the raw data table
        colNames = ["code_type", "code_issue_time", "code_str", "other_ldc_codes",
                    "code_description", "code_execution_time", "code_tags",
                    "code_issued_by", "code_issued_to", "pwc_element_id",
                    "pwc_element_type_id", "pwc_element_name", "pwc_element_type"]

        code_type = "Element"

        if code_issue_time == None:
            code_issue_time = dt.datetime.now()

        sqlVals = [code_type, code_issue_time, code_str, other_ldc_codes,
                   code_description, code_execution_time, code_tags,
                   code_issued_by, code_issued_to, pwc_element_id,
                   pwc_element_type_id, pwc_element_name, pwc_element_type]

        # get cursor for raw data table
        dbCur = dbConn.cursor()

        # text for sql place holders
        sqlPlaceHldrsTxt = ','.join([':{0}'.format(x+1)
                                     for x in range(len(colNames))])

        # insert the code
        codeInsSql = 'insert into code_book.op_codes({0}) values ({1})'.format(
            ','.join(colNames), sqlPlaceHldrsTxt)

        dbCur.execute(codeInsSql, sqlVals)

        # commit the changes
        dbConn.commit()
    except Exception as err:
        isInsertSuccess = False
        print('Error while creation of element code')
        print(err)
    finally:
        # closing database cursor and connection
        if dbCur is not None:
            dbCur.close()
        if dbConn is not None:
            dbConn.close()
    return isInsertSuccess
