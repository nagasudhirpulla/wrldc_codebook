import cx_Oracle
import datetime as dt
from typing import Optional, List, Tuple, Any
from src.repos.codes.getCodeById import getCodeById
from src.repos.codes.getGenericCodeChanges import getGenericCodeChanges
from src.app.externalOutages.getReasonId import getReasonId
from src.typeDefs.code import ICode
from src.app.externalOutages.checkIfOutageIsPresent import checkIfOutageIsPresent
from src.app.externalOutages.updateRtoRevivalData import updateRtoRevivalData
from src.app.externalOutages.checkIfElementIsOut import checkIfElementIsOut


def editElementRevivalCode(appDbConnStr: str, pwcDbConnStr: str, codeId: int, code_issue_time: Optional[dt.datetime],
                           code_str: str, other_ldc_codes: str,
                           code_description: str, code_execution_time: dt.datetime,
                           code_tags: str, code_issued_by: str, code_issued_to: str,
                           is_code_cancelled: bool, pwc_rto_id: int) -> bool:
    """updates an element outage code into the app db
    * If rtoId is null, then the data is corrupted
    * check for code existence by rtoId and update the isDelAtSrc flag
    Note: The revival time cannot be cleared once it is entered
    Returns:
        bool: returns true if process is ok
    """
    code: ICode = getCodeById(appDbConnStr, codeId)

    changedInfo: List[Tuple[str, Any]] = getGenericCodeChanges(code, code_issue_time,
                                                               code_str, other_ldc_codes,
                                                               code_description, code_execution_time,
                                                               code_tags, code_issued_by, code_issued_to,
                                                               is_code_cancelled)

    rtoId = code["pwcRtoId"]
    elName = code["pwcElName"]
    elId = code["pwcElId"]
    elTypeId = code["pwcElTypeId"]
    isRtoProcessOk = True

    # check if we can update the rto row in pwc db
    isCodeDeletedAtSrc = False if code["isDelAtSrc"] == 0 else True
    if (not isCodeDeletedAtSrc) and (not rtoId == None):
        # check again if outage w.r.t code is deleted in pwc db
        # and then update the isCodeDeletedAtSrc variable
        isCodeDeletedAtSrc = not checkIfOutageIsPresent(
            pwcDbConnStr, rtoId)
        if isCodeDeletedAtSrc:
            # set the flag in app db to represent that pwc outage entry in rto table is deleted
            changedInfo.append(("is_deleted_at_src", 1))
        else:
            # update real time outage revival data in pwc db
            isRtoUpdateSuccess = updateRtoRevivalData(
                pwcDbConnStr=pwcDbConnStr, rtoId=rtoId, revivalDt=code_execution_time, remarks=code_description)
            # if we could not edit the rto entry in pwc db,
            # we will mark the code editing operation as a failure
            isRtoProcessOk = True if isRtoUpdateSuccess else False
            if not isRtoProcessOk:
                print("could not edit element outage code for element {0} with element id = {1}, element type id = {2}, rto id = {3} since we could not edit the revival data in pwc db".format(
                    elName, elId, elTypeId, rtoId))

    if not isRtoProcessOk:
        # do not perform operations on app db if we could not update the pwc db correctly
        return False

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
    except Exception as err:
        isEditSuccess = False
        print('Error while updating of element revival code')
        print(err)
    finally:
        # closing database cursor and connection
        if dbCur is not None:
            dbCur.close()
        if dbConn is not None:
            dbConn.close()
    return isEditSuccess
