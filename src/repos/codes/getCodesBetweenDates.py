import cx_Oracle
import datetime as dt
from typing import List
from src.typeDefs.code import ICode


def getCodesBetweenDates(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime) -> List[ICode]:
    """fetches codes between 2 dates from app db

    Args:
        appDbConnStr (str): app db connection string
        startDt (dt.datetime): [description]
        endDt (dt.datetime): [description]

    Returns:
        List[ICode]: list of code objects
    """
    targetColumns = ['ID', 'CODE_TYPE', 'CODE_ISSUE_TIME', 'CODE_STR', 'OTHER_LDC_CODES',
                     'CODE_DESCRIPTION', 'CODE_EXECUTION_TIME', 'CODE_TAGS', 'CODE_ISSUED_BY',
                     'IS_CODE_CANCELLED', 'PWC_SD_REQ_ID', 'PWC_RTO_ID', 'IS_DELETED_AT_SRC',
                     'PWC_ELEMENT_ID', 'PWC_ELEMENT_TYPE_ID', 'PWC_OUTAGE_TYPE_ID',
                     'PWC_ELEMENT_NAME', 'PWC_ELEMENT_TYPE', 'PWC_OUTAGE_TYPE', 'CREATED_AT',
                     'UPDATED_AT', 'CODE_ISSUED_TO']

    codesFetchSql = """
            select {0}
            from code_book.op_codes 
            where is_deleted=0 
            and TRUNC(code_issue_time) between TRUNC(:1) and TRUNC(:2)
            order by code_issue_time desc
        """.format(','.join(targetColumns))

    # get connection with raw data table
    dbConn = cx_Oracle.connect(appDbConnStr)

    # get cursor and execute fetch sql
    dbCur = dbConn.cursor()
    dbCur.execute(codesFetchSql, (startDt, endDt))

    colNames = [row[0] for row in dbCur.description]

    if (False in [(col in targetColumns) for col in colNames]):
        # all desired columns not fetched, hence return empty
        return []

    # fetch all rows
    dbRows = dbCur.fetchall()

    # initialise codes to be returned
    codes: List[ICode] = []

    # iterate through each row to populate result outage rows
    for row in dbRows:
        id: ICode["id"] = row[colNames.index('ID')]
        codeType: ICode["codeType"] = row[colNames.index('CODE_TYPE')]
        codeIssueTime: ICode["codeIssueTime"] = row[colNames.index(
            'CODE_ISSUE_TIME')]
        codeStr: ICode["codeStr"] = row[colNames.index('CODE_STR')]
        otherLdcCodes: ICode["otherLdcCodes"] = row[colNames.index(
            'OTHER_LDC_CODES')]
        codeIssuedTo: ICode["codeIssuedTo"] = row[colNames.index(
            'CODE_ISSUED_TO')]
        codeDesc: ICode["codeDesc"] = row[colNames.index('CODE_DESCRIPTION')]
        codeExecTime: ICode["codeExecTime"] = row[colNames.index(
            'CODE_EXECUTION_TIME')]
        codeIssuedBy: ICode["codeIssuedBy"] = row[colNames.index(
            'CODE_ISSUED_BY')]
        codeTags: ICode["codeTags"] = row[colNames.index('CODE_TAGS')]
        isCodeCancelled: ICode["isCodeCancelled"] = row[colNames.index(
            'IS_CODE_CANCELLED')]
        pwcSdReqId: ICode["pwcSdReqId"] = row[colNames.index('PWC_SD_REQ_ID')]
        pwcRtoId: ICode["pwcRtoId"] = row[colNames.index('PWC_RTO_ID')]
        isDelAtSrc: ICode["isDelAtSrc"] = row[colNames.index(
            'IS_DELETED_AT_SRC')]
        pwcElId: ICode["pwcElId"] = row[colNames.index('PWC_ELEMENT_ID')]
        pwcElTypeId: ICode["pwcElTypeId"] = row[colNames.index(
            'PWC_ELEMENT_TYPE_ID')]
        pwcOutageTypeId: ICode["pwcOutageTypeId"] = row[colNames.index(
            'PWC_OUTAGE_TYPE_ID')]
        pwcElName: ICode["pwcElName"] = row[colNames.index('PWC_ELEMENT_NAME')]
        pwcElType: ICode["pwcElType"] = row[colNames.index('PWC_ELEMENT_TYPE')]
        pwcOutageType: ICode["pwcOutageType"] = row[colNames.index(
            'PWC_OUTAGE_TYPE')]
        createdAt: ICode["createdAt"] = row[colNames.index('CREATED_AT')]
        updatedAt: ICode["updatedAt"] = row[colNames.index('UPDATED_AT')]
        code: ICode = {
            "id": id,
            "codeType": codeType,
            "codeIssueTime": codeIssueTime,
            "codeStr": codeStr,
            "otherLdcCodes": otherLdcCodes,
            "codeIssuedTo": codeIssuedTo,
            "codeDesc": codeDesc,
            "codeExecTime": codeExecTime,
            "codeIssuedBy": codeIssuedBy,
            "isCodeCancelled": isCodeCancelled,
            "pwcSdReqId": pwcSdReqId,
            "isDelAtSrc": isDelAtSrc,
            "pwcElId": pwcElId,
            "pwcElTypeId": pwcElTypeId,
            "pwcOutageTypeId": pwcOutageTypeId,
            "pwcElName": pwcElName,
            "pwcElType": pwcElType,
            "pwcOutageType": pwcOutageType,
            "createdAt": createdAt,
            "updatedAt": updatedAt,
        }
        codes.append(code)
    return codes
