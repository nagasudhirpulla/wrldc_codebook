import datetime as dt
import cx_Oracle
from src.app.externalOutages.getReasonId import getReasonId
from typing import List, Tuple, Any
import datetime as dt


def updateRtoRevivalData(pwcDbConnStr: str, rtoId: int, revivalDt: dt.datetime,
                         remarks: str) -> bool:
    isEditSuccess = True
    # check for valid rto id
    if rtoId == None or rtoId < 1:
        return False

    updateInfo: List[Tuple[str, Any]] = []
    # check for valid reason
    if not(remarks == None) and not(remarks == ""):
        updateInfo.append(("REVIVAL_REMARKS", remarks))

    updateInfo.append(("MODIFIED_DATE", dt.datetime.now()))

    # check for valid outage date
    if not revivalDt == None:
        revivalDate: dt.datetime = dt.datetime(
            revivalDt.year, revivalDt.month, revivalDt.day)
        revivalTime: str = dt.datetime.strftime(revivalDt, "%H:%M")
        updateInfo.append(("REVIVED_DATE", revivalDate))
        updateInfo.append(("REVIVED_TIME", revivalTime))

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
        print('Error while updating real time outage entry revival data in pwc table')
        print(err)
    finally:
        # closing database cursor and connection
        if dbCur is not None:
            dbCur.close()
        if dbConn is not None:
            dbConn.close()
    return isEditSuccess
