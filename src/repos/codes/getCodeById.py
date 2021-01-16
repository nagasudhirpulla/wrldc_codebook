import cx_Oracle
import datetime as dt
from typing import List, Optional
from src.typeDefs.code import ICode


def getCodeById(appDbConnStr: str, codeId: int) -> Optional[ICode]:
    """fetches codes between 2 dates from app db

    Args:
        appDbConnStr (str): app db connection string
        codeId (int): [description]

    Returns:
        Optional[ICode]: code object
    """
    targetColumns = ['ID', 'CODE_TYPE', 'CODE_ISSUE_TIME', 'CODE_STR', 'OTHER_LDC_CODES',
                     'CODE_DESCRIPTION', 'CODE_EXECUTION_TIME', 'CODE_TAGS', 'CODE_ISSUED_BY',
                     'IS_CODE_CANCELLED', 'PWC_SD_REQ_ID', 'PWC_RTO_ID', 'IS_DELETED_AT_SRC',
                     'PWC_ELEMENT_ID', 'PWC_ELEMENT_TYPE_ID', 'PWC_OUTAGE_TYPE_ID', 'PWC_OUTAGE_TAG_ID',
                     'PWC_ELEMENT_NAME', 'PWC_ELEMENT_TYPE', 'PWC_OUTAGE_TYPE', 'PWC_OUTAGE_TAG',
                     'CREATED_AT', 'UPDATED_AT', 'CODE_ISSUED_TO']

    codesFetchSql = """
            select {0}
            from code_book.op_codes 
            where id=:1
        """.format(','.join(targetColumns))

    # initialise code object
    code: Optional[ICode] = None
    colNames = []
    dbRows = []
    dbConn = None
    dbCur = None
    try:
        # get connection with raw data table
        dbConn = cx_Oracle.connect(appDbConnStr)

        # get cursor and execute fetch sql
        dbCur = dbConn.cursor()
        dbCur.execute(codesFetchSql, (codeId,))

        colNames = [row[0] for row in dbCur.description]

        # fetch all rows
        dbRows = dbCur.fetchall()
    except Exception as err:
        dbRows = []
        print('Error while creation of fetching code by Id')
        print(err)
    finally:
        # closing database cursor and connection
        if dbCur is not None:
            dbCur.close()
        if dbConn is not None:
            dbConn.close()
    
    if (False in [(col in targetColumns) for col in colNames]):
            # all desired columns not fetched, hence return empty
            return None
    
    if len(dbRows) == 0:
        return code

    row = dbRows[0]
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
    pwcOutageTagId: ICode["pwcOutageTagId"] = row[colNames.index(
            'PWC_OUTAGE_TAG_ID')]
    pwcElName: ICode["pwcElName"] = row[colNames.index('PWC_ELEMENT_NAME')]
    pwcElType: ICode["pwcElType"] = row[colNames.index('PWC_ELEMENT_TYPE')]
    pwcOutageType: ICode["pwcOutageType"] = row[colNames.index(
        'PWC_OUTAGE_TYPE')]
    pwcOutageTag: ICode["pwcOutageTag"] = row[colNames.index(
            'PWC_OUTAGE_TAG')]
    createdAt: ICode["createdAt"] = row[colNames.index('CREATED_AT')]
    updatedAt: ICode["updatedAt"] = row[colNames.index('UPDATED_AT')]
    code = {
        "id": id,
        "codeType": codeType,
        "codeIssueTime": codeIssueTime,
        "codeStr": codeStr,
        "otherLdcCodes": otherLdcCodes,
        "codeIssuedTo": codeIssuedTo,
        "codeDesc": codeDesc,
        "codeExecTime": codeExecTime,
        "codeIssuedBy": codeIssuedBy,
        "codeTags": codeTags,
        "isCodeCancelled": isCodeCancelled,
        "pwcSdReqId": pwcSdReqId,
        "pwcRtoId": pwcRtoId,
        "isDelAtSrc": isDelAtSrc,
        "pwcElId": pwcElId,
        "pwcElTypeId": pwcElTypeId,
        "pwcOutageTypeId": pwcOutageTypeId,
        "pwcOutageTagId": pwcOutageTagId,
        "pwcElName": pwcElName,
        "pwcElType": pwcElType,
        "pwcOutageType": pwcOutageType,
        "pwcOutageTag": pwcOutageTag,
        "createdAt": createdAt,
        "updatedAt": updatedAt
    }
    return code
