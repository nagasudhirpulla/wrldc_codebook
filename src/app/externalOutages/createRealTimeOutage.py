import datetime as dt
from typing import Optional, cast
import cx_Oracle
from src.app.externalOutages.getReasonId import getReasonId


def createRealTimeOutage(pwcDbConnStr: str, elemTypeId: int, elementId: int, outageDt: dt.datetime, outageTypeId: int,
                         reason: str, elementName: str, sdReqId: int, outageTagId: int, expectedRevivalDt: Optional[dt.datetime] = None) -> int:
    """create a new row in real time outages pwc table and return the id of newly created row

    Args:
        pwcDbConnStr (str): [description]
        elemTypeId (int): [description]
        elementId (int): [description]
        outageDt (dt.datetime): [description]
        outageTypeId (int): [description]
        reason (str): [description]
        elementName (str): [description]
        sdReqId (int): [description]
        outageTagId (int): [description]

    Returns:
        int: id of newly created row
    """    
    newRtoId = -1
    if outageDt == None:
        return -1
    if reason == None or reason == "":
        reason = "NA"
    reasId = getReasonId(pwcDbConnStr, reason, outageTypeId)
    if reasId == -1:
        return -1
    outageDate: dt.datetime = dt.datetime(
        outageDt.year, outageDt.month, outageDt.day)
    outageTime: str = dt.datetime.strftime(outageDt, "%H:%M")

    expectedRevivalDate:Optional[dt.datetime] = None
    expectedRevivalTime:Optional[str] = None
    if not expectedRevivalDt == None:
        expRevDt = cast(dt.datetime, expectedRevivalDt)
        expectedRevivalDate = dt.datetime(expRevDt.year, expRevDt.month, expRevDt.day)
        expectedRevivalTime = dt.datetime.strftime(expRevDt, "%H:%M")

    newRtoIdFetchSql = """
    SELECT MAX(rto.ID)+1 FROM REPORTING_WEB_UI_UAT.real_time_outage rto
    """

    rtoInsertSql = """
    insert into reporting_web_ui_uat.real_time_outage rto(ID, ENTITY_ID, ELEMENT_ID, OUTAGE_DATE, 
    OUTAGE_TIME, RELAY_INDICATION_SENDING_ID, RELAY_INDICATION_RECIEVING_ID, CREATED_DATE, 
    SHUT_DOWN_TYPE, REASON_ID, CREATED_BY, MODIFIED_BY, REGION_ID, ELEMENTNAME,
    SHUTDOWNREQUEST_ID, LOAD_AFFECTED, IS_LOAD_OR_GEN_AFFECTED, SHUTDOWN_TAG_ID, IS_DELETED, EXPECTED_DATE, EXPECTED_TIME) values 
    (:id, :elemTypeId, :elementId, :outageDate, :outageTime, 0, 0, CURRENT_TIMESTAMP, :outageTypeId, 
    :reasonId, 123, 123, 4, :elementName, :sdReqId, 0, 0, :outageTagId, NULL, :expectedDate, :expectedTime)
    """

    dbConn = None
    dbCur = None
    try:
        # get connection with raw data table
        dbConn = cx_Oracle.connect(pwcDbConnStr)

        # get cursor for raw data table
        dbCur = dbConn.cursor()

        # execute the new rto id fetch sql
        dbCur.execute(newRtoIdFetchSql)
        dbRows = dbCur.fetchall()
        newRtoId = dbRows[0][0]

        sqlData = {"id": newRtoId, "elemTypeId": elemTypeId, "elementId": elementId,
                   "outageDate": outageDate, "outageTime": outageTime,
                   "outageTypeId": outageTypeId, "reasonId": reasId,
                   "elementName": elementName, "sdReqId": sdReqId,
                   "outageTagId": outageTagId, "expectedDate": expectedRevivalDate,
                   "expectedTime": expectedRevivalTime}

        # execute the new row insertion sql
        dbCur.execute(rtoInsertSql, sqlData)

        # commit the changes
        dbConn.commit()
    except Exception as e:
        newRtoId = -1
        print('Error while creating new real time outage entry in pwc table')
        print(e)
    finally:
        # closing database cursor and connection
        if dbCur is not None:
            dbCur.close()
        if dbConn is not None:
            dbConn.close()
    return newRtoId
