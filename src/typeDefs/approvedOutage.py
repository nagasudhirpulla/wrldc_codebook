from typing import TypedDict
import datetime as dt


class IApprovedOutage(TypedDict):
    sdId: int
    sdReqId: int
    elTypeId: int
    elId: int
    elName: str
    elType: str
    reasonId: int
    reason: str
    outageType: str
    outageTypeId: int
    occName: str
    requester: str
    dailyCont: str
    approvedStartDt: str
    approvedEndDt: str
    requesterRemarks: str
    availingStatus: str
    approvalStatus: str
    rldcRemarks: str
    rpcRemarks: str
    nldcRemarks: str
