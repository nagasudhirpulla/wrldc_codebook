import cx_Oracle
import datetime as dt
from typing import Optional, List, Tuple, Any
from src.repos.codes.getCodeById import getCodeById
from src.repos.codes.getGenericCodeChanges import getGenericCodeChanges
from src.repos.codes.getElementOutageCodeChanges import getElementOutageCodeChanges
from src.repos.outages.getExpectedRevivalTime import getExpectedRevivalTime
from src.typeDefs.code import ICode
from src.app.externalOutages.checkIfOutageIsPresent import checkIfOutageIsPresent
from src.app.externalOutages.createRealTimeOutage import createRealTimeOutage
from src.app.externalOutages.updateRealTimeOutage import updateRealTimeOutage
from src.app.externalOutages.checkIfElementIsOut import checkIfElementIsOut


def editElementOutageCode(appDbConnStr: str, pwcDbConnStr: str, codeId: int, code_issue_time: Optional[dt.datetime],
                          code_str: str, other_ldc_codes: str,
                          code_description: str, code_execution_time: dt.datetime,
                          code_tags: str, code_issued_by: str, code_issued_to: str,
                          is_code_cancelled: bool, pwc_outage_type_id: int,
                          pwc_outage_tag_id: int, pwc_outage_type: str,
                          pwc_outage_tag: str) -> bool:
    """updates an element outage code into the app db
    case 1 - create new code in pwc db
    criteria - (rto_id of code is None) and (execution time of code was None and now present)

    case 2 - update code in pwc db
    criteria - (rto_id of code is present) and (outage w.r.t code is not deleted in pwc db)
    Note - outage cannot be created in code book if element is already out
    Returns:
        bool: returns true if process is ok
    """
    code: ICode = getCodeById(appDbConnStr, codeId)

    changedInfo: List[Tuple[str, Any]] = getGenericCodeChanges(code, code_issue_time,
                                                               code_str, other_ldc_codes,
                                                               code_description, code_execution_time,
                                                               code_tags, code_issued_by, code_issued_to,
                                                               is_code_cancelled)
    changedInfo.extend(getElementOutageCodeChanges(code, pwc_outage_type_id,
                                                   pwc_outage_tag_id,
                                                   pwc_outage_type, pwc_outage_tag))

    rtoId = code["pwcRtoId"]
    elName = code["pwcElName"]
    elId = code["pwcElId"]
    elTypeId = code["pwcElTypeId"]
    sdReqId = 0
    if code["codeType"] == "ApprovedOutage":
        sdReqId = code["pwcSdReqId"]
    isRtoProcessOk = True
    if (rtoId == None) and (code["codeExecTime"] == None) and not(code_execution_time == None):
        # check if element is already out
        isElOut = checkIfElementIsOut(
            pwcDbConnStr=pwcDbConnStr, elId=elId, elTypeId=elTypeId)
        if isElOut:
            # element is already out, hence this is not a valid code editing operation
            isRtoProcessOk = False
            print("could not edit element outage code for element {0} with element id = {1}, element type id = {2}, since element is already out".format(
                elName, elId, elTypeId))
        else:
            expectedRevDt:Optional[dt.datetime] = None
            if sdReqId > 0:
                expectedRevDt = getExpectedRevivalTime(pwcDbConnStr=pwcDbConnStr, sdReqId=sdReqId)
            newRtoId = createRealTimeOutage(
                pwcDbConnStr=pwcDbConnStr, elemTypeId=elTypeId,
                elementId=elId, outageDt=code_execution_time, outageTypeId=pwc_outage_type_id,
                reason=code_description, elementName=elName, sdReqId=sdReqId,
                outageTagId=pwc_outage_tag_id, expectedRevivalDt=expectedRevDt)
            if newRtoId > 0:
                changedInfo.append(("pwc_rto_id", newRtoId))
            else:
                # we could not create a new rto entry in vendor db,
                # hence this is not a valid code editing operation
                isRtoProcessOk = False
                print("could not edit element outage code for element {0} with element id = {1}, element type id = {2}, since we could not create a new outage entry in pwc db".format(
                    elName, elId, elTypeId))
    else:
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
                # update real time outage in pwc db
                isRtoUpdateSuccess = updateRealTimeOutage(
                    pwcDbConnStr=pwcDbConnStr, rtoId=rtoId, outageDt=code_execution_time, outageTypeId=pwc_outage_type_id,
                    reason=code_description, outageTagId=pwc_outage_tag_id)
                # if we could not edit the rto entry in pwc db,
                # we will mark the code editing operation as a failure
                isRtoProcessOk = True if isRtoUpdateSuccess else False
                if not isRtoProcessOk:
                    print("could not edit element outage code for element {0} with element id = {1}, element type id = {2}, since we could not edit the outage entry in pwc db".format(
                        elName, elId, elTypeId))

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
        print('Error while updating of element outage code')
        print(err)
    finally:
        # closing database cursor and connection
        if dbCur is not None:
            dbCur.close()
        if dbConn is not None:
            dbConn.close()
    return isEditSuccess
