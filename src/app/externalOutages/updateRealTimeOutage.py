import datetime as dt
import cx_Oracle
from src.app.externalOutages.getReasonId import getReasonId
from typing import List, Tuple, Any
import datetime as dt


def updateRealTimeOutage(pwcDbConnStr: str, rtoId: int, outageDt: dt.datetime,
                         outageTypeId: int, reason: str, outageTagId: int) -> bool:
    isEditSuccess = True
    # check for valid rto id
    if rtoId == None or rtoId < 1:
        return False
    # check for valid reason
    if reason == None or reason == "":
        reason = "NA"
    reasId = getReasonId(pwcDbConnStr, reason, outageTypeId)
    if reasId == -1:
        return False

    updateInfo: List[Tuple[str, Any]] = []
    updateInfo.append(("REASON_ID", reasId))
    updateInfo.append(("SHUT_DOWN_TYPE", outageTypeId))
    updateInfo.append(("SHUTDOWN_TAG_ID", outageTagId))
    updateInfo.append(("MODIFIED_DATE", dt.datetime.now()))

    # check for valid outage date
    if not outageDt == None:
        outageDate: dt.datetime = dt.datetime(
            outageDt.year, outageDt.month, outageDt.day)
        outageTime: str = dt.datetime.strftime(outageDt, "%H:%M")
        updateInfo.append(("OUTAGE_DATE", outageDate))
        updateInfo.append(("OUTAGE_TIME", outageTime))

    sqlSetString = ','.join(["{0}=:{1}".format(uInf[0], iInd+1)
                             for iInd, uInf in enumerate(updateInfo)])

    rtoUpdateSql = """
    update reporting_web_ui_uat.real_time_outage rto set {0} where rto.id=:{1}
    """.format(sqlSetString, len(updateInfo)+1)

    updateVals: List[Any] = [uInf[1] for uInf in updateInfo]
    updateVals.append(rtoId)

    dbConn = None
    dbCur = None
    try:
        # get connection with raw data table
        dbConn = cx_Oracle.connect(pwcDbConnStr)

        # get cursor for raw data table
        dbCur = dbConn.cursor()

        # run rto update sql
        dbCur.execute(rtoUpdateSql, updateVals)

        # commit the changes
        dbConn.commit()
    except Exception as err:
        isEditSuccess = False
        print('Error while updating real time outage entry in pwc table')
        print(err)
    finally:
        # closing database cursor and connection
        if dbCur is not None:
            dbCur.close()
        if dbConn is not None:
            dbConn.close()
    return isEditSuccess
