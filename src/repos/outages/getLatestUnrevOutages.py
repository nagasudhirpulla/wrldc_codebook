from src.typeDefs.unRevOutage import IUnRevOutage
from typing import List
import cx_Oracle
from src.app.utils.getTimeDeltaFromDbStr import getTimeDeltaFromDbStr


def getLatestUnrevOutages(pwcDbConnStr: str) -> List[IUnRevOutage]:
    fetchSql = """SELECT
        rto.id,
        rto.entity_id,
        rto.element_id,
        rto.entity_name AS elementType,
        rto.SHUT_DOWN_TYPE_NAME,
        rto.elementname,
        trunc(rto.outage_date) AS outage_date,
        rto.outage_time,
        rto.reason,
        rto.shutdown_tag,
        rto.outage_remarks
    FROM
        (
        SELECT
            outages.*, ent_master.ENTITY_NAME, reas.reason, sd_type.name AS SHUT_DOWN_TYPE_NAME, sd_tag.name AS shutdown_tag, to_char(outages.OUTAGE_DATE , 'YYYY-MM-DD')|| ' ' || outages.OUTAGE_TIME AS out_date_time
        FROM
            reporting_web_ui_uat.REAL_TIME_OUTAGE outages
        LEFT JOIN reporting_web_ui_uat.outage_reason reas ON
            reas.id = outages.reason_id AND reas.OUTAGE_TYPE_ID = outages.shut_down_type
        LEFT JOIN reporting_web_ui_uat.entity_master ent_master ON
            ent_master.id = outages.ENTITY_ID
        LEFT JOIN reporting_web_ui_uat.shutdown_outage_tag sd_tag ON
            sd_tag.id = outages.SHUTDOWN_TAG_ID
        LEFT JOIN reporting_web_ui_uat.shutdown_outage_type sd_type ON
            sd_type.id = outages.shut_down_type ) rto
    INNER JOIN (
        SELECT
            element_id, entity_id, MAX(to_char(OUTAGE_DATE , 'YYYY-MM-DD')|| ' ' || OUTAGE_TIME) AS out_date_time
        FROM
            reporting_web_ui_uat.REAL_TIME_OUTAGE
        GROUP BY
            entity_id, ELEMENT_ID) latest_out_info ON
        ((latest_out_info.entity_id = rto.entity_id)
        AND (latest_out_info.element_id = rto.element_id)
        AND (latest_out_info.out_date_time = rto.out_date_time))
    WHERE rto.REVIVED_TIME IS NULL
    ORDER BY
        rto.out_date_time DESC"""
    targetColumns = ['ID', 'ENTITY_ID', 'ELEMENT_ID', 'ELEMENTTYPE',
                     'SHUT_DOWN_TYPE_NAME', 'ELEMENTNAME', 'OUTAGE_DATE',
                     'OUTAGE_TIME', 'REASON', 'SHUTDOWN_TAG', 'OUTAGE_REMARKS']
    outages: List[IUnRevOutage] = []
    colNames = []
    dbRows = []
    dbConn = None
    dbCur = None
    try:
        # get connection with raw data table
        dbConn = cx_Oracle.connect(pwcDbConnStr)

        # get cursor and execute fetch sql
        dbCur = dbConn.cursor()
        dbCur.execute(fetchSql)

        colNames = [row[0] for row in dbCur.description]

        dbRows = dbCur.fetchall()
    except Exception as err:
        dbRows = []
        print('Error while getting latest unrevived real time outages from pwc db')
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
        outTimeStr = row[colNames.index("OUTAGE_TIME")]
        outTimeDelta = getTimeDeltaFromDbStr(outTimeStr)
        # strip off hours and minute components
        outageDt = row[colNames.index("OUTAGE_DATE")]
        outageDt = outageDt.replace(
            hour=0, minute=0, second=0, microsecond=0)
        # add out time to out date to get outage timestamp
        outageDt += outTimeDelta
        outage: IUnRevOutage = {
            "rtoId": row[colNames.index("ID")],
            "elTypeId": row[colNames.index("ENTITY_ID")],
            "elId": row[colNames.index("ELEMENT_ID")],
            "elType": row[colNames.index("ELEMENTTYPE")],
            "outageType": row[colNames.index("SHUT_DOWN_TYPE_NAME")],
            "elName": row[colNames.index("ELEMENTNAME")],
            "outageDt": outageDt,
            "reason": row[colNames.index("REASON")],
            "outageTag": row[colNames.index("SHUTDOWN_TAG")],
            "outageRemarks": row[colNames.index("OUTAGE_REMARKS")]
        }
        outages.append(outage)

    return outages
