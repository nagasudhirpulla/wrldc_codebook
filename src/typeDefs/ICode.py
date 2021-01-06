from typing import TypedDict
import datetime as dt


class ICode(TypedDict):
    id: int
    codeType: str
    codeIssueTime: dt.datetime
    codeStr: str
    otherLdcCodes: str
    codeIssuedTo: str
    codeDescription: str
    codeExecutionTime: dt.datetime
    codeIssuedBy: str
    codeTags: str
    isCodeCancelled: int
    pwcSdReqId: int
    pwcRtoId: int
    isDeletedAtSrc: int
    pwcElementId: int
    pwcElementTypeId: int
    pwcOutageTypeId: str
    pwcElementName: str
    pwcElementType: str
    pwcOutageType: str
    createdAt: dt.datetime
    updatedAt: dt.datetime
