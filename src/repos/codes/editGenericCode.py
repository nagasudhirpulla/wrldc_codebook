import cx_Oracle
import datetime as dt
from typing import Optional, List, Tuple, Any
from src.repos.codes.codesRepo import CodesRepo
from src.typeDefs.code import ICode


def editGenericCode(appDbConnStr: str, code_id: int, code_issue_time: Optional[dt.datetime],
                    code_str: str, other_ldc_codes: str,
                    code_description: str, code_execution_time: dt.datetime,
                    code_tags: str, code_issued_by: str, code_issued_to: str, is_code_cancelled: bool) -> bool:
    """inserts a generic code into the app db
    Returns:
        bool: returns true if process is ok
    """
    cRepo = CodesRepo(appDbConnStr)
    code: ICode = cRepo.getCodeById(code_id)

    changedInfo: List[Tuple[str, Any]] = []

    # check if codeIssueTime has changed
    if not code["codeIssueTime"] == code_issue_time:
        changedInfo.append(("code_issue_time", code_issue_time))

    # check if code_str has changed
    if not code["codeStr"] == code_str:
        changedInfo.append(("code_str", code_str))

    # check if other ldc codes has changed
    if not code["otherLdcCodes"] == other_ldc_codes:
        changedInfo.append(("other_ldc_codes", other_ldc_codes))

    # check if code issued to has changed
    if not code["codeIssuedTo"] == code_issued_to:
        changedInfo.append(("code_issued_to", code_issued_to))

    # check if code Description has changed
    if not code["codeDesc"] == code_description:
        changedInfo.append(("code_description", code_description))

    # check if code execution time has changed
    if not code["codeExecTime"] == code_execution_time:
        changedInfo.append(("code_execution_time", code_execution_time))

    # check if code issued by has changed
    if not code["codeIssuedBy"] == code_issued_by:
        changedInfo.append(("code_issued_by", code_issued_by))

    # check if code tags has changed
    if not code["codeTags"] == code_tags:
        changedInfo.append(("code_tags", code_tags))

    # check if is code cancelled has changed
    originalCodeCancelFlag = False if code["isCodeCancelled"] == 0 else True
    if not originalCodeCancelFlag == is_code_cancelled:
        changedInfo.append(("is_code_cancelled", is_code_cancelled))

    isEditSuccess = True
    if len(changedInfo) == 0:
        return isEditSuccess

    # get connection with raw data table
    dbConn = cx_Oracle.connect(appDbConnStr)

    try:
        sqlSetString = ','.join(["{0}={1}".format(iInd+1, cInf[0])
                                 for iInd, cInf in enumerate(changedInfo)])

        # get cursor for raw data table
        dbCur = dbConn.cursor()

        # edit the code
        codeEditSql = 'update code_book.op_codes set {0} where id={1}'.format(
            sqlSetString, len(changedInfo)+1)

        sqlVals: List[Any] = [cInf[1] for cInf in changedInfo]
        sqlVals.append(code_id)

        dbCur.execute(codeEditSql, sqlVals)

        # commit the changes
        dbConn.commit()
    except Exception as e:
        isEditSuccess = False
        print('Error while creation of generic code')
        print(e)
    finally:
        # closing database cursor and connection
        if dbCur is not None:
            dbCur.close()
        dbConn.close()
    return isEditSuccess
