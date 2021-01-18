from src.typeDefs.approvedOutage import IApprovedOutage
from typing import List
import cx_Oracle
from src.app.utils.getTimeDeltaFromDbStr import getTimeDeltaFromDbStr
import datetime as dt


def getApprovedOutages(pwcDbConnStr: str, targetDt: dt.datetime) -> List[IApprovedOutage]:
    fetchSql = """
    SELECT
        SD.ID,
        SD.SHUTDOWN_REQUEST_ID,
        sr.ENTITY_ID,
        sr.ELEMENT_ID,
        sr.REASON_ID,
        sr.shutdownType,
        sr.SHUT_DOWN_TYPE_ID,
        sr.	SHUTDOWN_TAG_ID,
        sr.SHUTDOWN_TAG,
        sr.occ_name,
        sr.elementType,
        sr.ELEMENT_NAME,
        sr.requester_name,
    CASE
            WHEN SR.IS_CONTINUOUS = 1 THEN 'Continuous'
            WHEN sr.IS_CONTINUOUS = 0 THEN 'Daily'
            ELSE NULL
        END DailyCont,
        sr.REASON,
        SD.APPROVED_START_DATE,
        SD.APPROVED_END_DATE,
        sr.REQUESTER_REMARKS,
    CASE
            WHEN sr.is_availed = 1 THEN 'Yes'
            WHEN sr.is_availed = 2 THEN 'NO'
            ELSE NULL
        END AvailingStatus,
        ss.STATUS,
        SD.RLDC_REMARKS,
        sr.rpc_remarks,
        sr.NLDC_REMARKS,
        sr.nldc_approval_status
    FROM
        REPORTING_WEB_UI_UAT.SHUTDOWN sd
    LEFT JOIN REPORTING_WEB_UI_UAT.SHUTDOWN_STATUS ss ON
        ss.ID = sd.STATUS_ID
    LEFT JOIN (
        SELECT
            req.*, sot.NAME AS shutdownType, em.ENTITY_NAME AS elementType, or2.REASON, om.OCC_NAME, ud.USER_NAME AS requester_name, ss2.STATUS AS nldc_approval_status, sdTag.NAME AS SHUTDOWN_TAG
        FROM
            REPORTING_WEB_UI_UAT.SHUTDOWN_REQUEST req
        LEFT JOIN REPORTING_WEB_UI_UAT.SHUTDOWN_OUTAGE_TYPE sot ON
            sot.ID = req.SHUT_DOWN_TYPE_ID
        LEFT JOIN REPORTING_WEB_UI_UAT.ENTITY_MASTER em ON
            em.ID = req.ENTITY_ID
        LEFT JOIN REPORTING_WEB_UI_UAT.OUTAGE_REASON or2 ON
            or2.ID = req.REASON_ID
        LEFT JOIN REPORTING_WEB_UI_UAT.OCC_MASTER om ON
            om.OCC_ID = req.OCC_ID
        LEFT JOIN REPORTING_WEB_UI_UAT.USER_DETAILS ud ON
            req.INTENDED_BY = ud.USERID
        LEFT JOIN REPORTING_WEB_UI_UAT.SHUTDOWN_OUTAGE_TAG sdTag ON
            sdTag.ID = req.SHUTDOWN_TAG_ID 
        LEFT JOIN REPORTING_WEB_UI_UAT.SHUTDOWN_STATUS ss2 ON
            req.NLDC_STATUS_ID = ss2.ID ) sr ON
        sr.ID = sd.SHUTDOWN_REQUEST_ID
    WHERE
        (TRUNC(:1) BETWEEN TRUNC(sd.APPROVED_START_DATE) AND TRUNC(sd.APPROVED_END_DATE))
        AND ss.STATUS = 'Approved'
    """
    targetColumns = ['ID', 'SHUTDOWN_REQUEST_ID', 'ENTITY_ID', 'ELEMENT_ID',
                     'REASON_ID', 'SHUTDOWNTYPE', 'SHUT_DOWN_TYPE_ID', 'SHUTDOWN_TAG_ID',
                     'SHUTDOWN_TAG', 'OCC_NAME', 'ELEMENTTYPE', 'ELEMENT_NAME', 'REQUESTER_NAME',
                     'DAILYCONT', 'REASON', 'APPROVED_START_DATE', 'APPROVED_END_DATE',
                     'REQUESTER_REMARKS', 'AVAILINGSTATUS', 'STATUS', 'RLDC_REMARKS',
                     'RPC_REMARKS', 'NLDC_REMARKS', 'NLDC_APPROVAL_STATUS']
    outages: List[IApprovedOutage] = []
    colNames = []
    dbRows = []
    dbConn = None
    dbCur = None
    try:
        # get connection with raw data table
        dbConn = cx_Oracle.connect(pwcDbConnStr)

        # get cursor and execute fetch sql
        dbCur = dbConn.cursor()
        dbCur.execute(fetchSql, (targetDt,))

        colNames = [row[0] for row in dbCur.description]

        dbRows = dbCur.fetchall()
    except Exception as err:
        dbRows = []
        print('Error while getting approved outages from pwc db')
        print(err)
    finally:
        # closing database cursor and connection
        if dbCur is not None:
            dbCur.close()
        if dbConn is not None:
            dbConn.close()

    if (False in [(col in targetColumns) for col in colNames]):
        # all desired columns not fetched, hence return empty
        return outages

    # fetch all rows
    for row in dbRows:
        outage: IApprovedOutage = {
            "sdId": row[colNames.index("ID")],
            "sdReqId": row[colNames.index("SHUTDOWN_REQUEST_ID")],
            "elTypeId": row[colNames.index("ENTITY_ID")],
            "elId": row[colNames.index("ELEMENT_ID")],
            "elName": row[colNames.index("ELEMENT_NAME")],
            "elType": row[colNames.index("ELEMENTTYPE")],
            "reasonId": row[colNames.index("REASON_ID")],
            "reason": row[colNames.index("REASON")],
            "outageType": row[colNames.index("SHUTDOWNTYPE")],
            "outageTypeId": row[colNames.index("SHUT_DOWN_TYPE_ID")],
            "outageTag": row[colNames.index("SHUTDOWN_TAG")],
            "outageTagId": row[colNames.index("SHUTDOWN_TAG_ID")],
            "occName": row[colNames.index("OCC_NAME")],
            "requester": row[colNames.index("REQUESTER_NAME")],
            "dailyCont": row[colNames.index("DAILYCONT")],
            "approvedStartDt": row[colNames.index("APPROVED_START_DATE")],
            "approvedEndDt": row[colNames.index("APPROVED_END_DATE")],
            "requesterRemarks": row[colNames.index("REQUESTER_REMARKS")],
            "availingStatus": row[colNames.index("AVAILINGSTATUS")],
            "approvalStatus": row[colNames.index("STATUS")],
            "nldcApprovalStatus": row[colNames.index("NLDC_APPROVAL_STATUS")],
            "rldcRemarks": row[colNames.index("RLDC_REMARKS")],
            "rpcRemarks": row[colNames.index("RPC_REMARKS")],
            "nldcRemarks": row[colNames.index("NLDC_REMARKS")]
        }
        outages.append(outage)

    return outages
