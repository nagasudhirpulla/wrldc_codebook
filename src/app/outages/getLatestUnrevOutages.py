from src.repos.outages.outagesRepo import OutagesRepo
from src.repos.codes.codesRepo import CodesRepo
from src.typeDefs.unRevOutage import IUnRevOutageWithCode
from typing import List


def getLatestUnrevOutages(appDbConnStr: str, pwcDbConnStr: str) -> List[IUnRevOutageWithCode]:
    oRepo = OutagesRepo(pwcDbConnStr)
    outages = oRepo.getLatestUnrevOutages()
    cRepo = CodesRepo(appDbConnStr)
    rtoIds = [o['rtoId'] for o in outages]
    rtoCodes = cRepo.getCodesForRtoIds(rtoIds)
    for o in outages:
        o['code'] = ''
        rtoId = o['rtoId']
        if rtoId in rtoCodes:
            o['code'] = rtoCodes[rtoId]
    return outages
