import cx_Oracle
import datetime as dt
from typing import Optional, List, Tuple, Any
from src.repos.codes.getCodeById import getCodeById
from src.repos.codes.getGenericCodeChanges import getGenericCodeChanges
from src.typeDefs.code import ICode

def editElementCode(appDbConnStr: str, codeId: int, code_issue_time: Optional[dt.datetime],
                    code_str: str, other_ldc_codes: str,
                    code_description: str, code_execution_time: dt.datetime,
                    code_tags: str, code_issued_by: str, code_issued_to: str, is_code_cancelled: bool) -> bool:
    """updates a generic code into the app db
    Returns:
        bool: returns true if process is ok
    """
    code: ICode = getCodeById(appDbConnStr, codeId)

    changedInfo: List[Tuple[str, Any]] = getGenericCodeChanges(code, code_issue_time,
                                                               code_str, other_ldc_codes,
                                                               code_description, code_execution_time,
                                                               code_tags, code_issued_by, code_issued_to,
                                                               is_code_cancelled)

    isEditSuccess = True
    if len(changedInfo) == 0:
        return isEditSuccess
    dbConn = None
    dbCur = None
    try:
        # get connection with raw data table
        dbConn = cx_Oracle.connect(appDbConnStr)
        sqlSetString = ','.join(["{0}=:{1}".format(cInf[0], iInd+1)
                                 for iInd, cInf in enumerate(changedInfo)])

        # get cursor for raw data table
        dbCur = dbConn.cursor()

        # edit the code
        codeEditSql = 'update code_book.op_codes set {0} where id=:{1}'.format(
            sqlSetString, len(changedInfo)+1)

        sqlVals: List[Any] = [cInf[1] for cInf in changedInfo]
        sqlVals.append(codeId)

        dbCur.execute(codeEditSql, sqlVals)

        # commit the changes
        dbConn.commit()
    except Exception as e:
        isEditSuccess = False
        print('Error while updating of element code')
        print(e)
    finally:
        # closing database cursor and connection
        if dbCur is not None:
            dbCur.close()
        if dbConn is not None:
            dbConn.close()
    return isEditSuccess
