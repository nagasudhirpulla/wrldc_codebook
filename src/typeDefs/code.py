from typing import TypedDict, Optional
import datetime as dt


class ICode(TypedDict):
    id: int
    codeType: str
    codeIssueTime: dt.datetime
    codeStr: str
    otherLdcCodes: Optional[str]
    codeIssuedTo: str
    codeDesc: str
    codeExecTime: Optional[dt.datetime]
    codeIssuedBy: str
    codeTags: Optional[str]
    isCodeCancelled: int
    pwcSdReqId: Optional[int]
    pwcRtoId: Optional[int]
    isDelAtSrc: int
    pwcElId: Optional[int]
    pwcElTypeId: Optional[int]
    pwcOutageTypeId: Optional[int]
    pwcElName: Optional[str]
    pwcElType: Optional[str]
    pwcOutageType: Optional[str]
    createdAt: dt.datetime
    updatedAt: dt.datetime
