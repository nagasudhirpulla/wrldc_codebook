import requests
import datetime as dt
from flask import jsonify
from src.typeDefs.getCodeRequestResp import IGetCodeRequestResp


class UpdateCodeRequestApiHandler():
    UpdateCodeRequestApiUrl = ''

    def __init__(self, UpdateCodeRequestApiUrl):
        self.UpdateCodeRequestApiUrl = UpdateCodeRequestApiUrl

    def updateCodeRequest(self, codeReqId: int, isApproved: bool, code: str) -> IGetCodeRequestResp:
        """update latest code request using the api service
        Args:
            codeReqId (int) : codeReqId
            isApproved (bool) : approval status
            code (string) : code string from code book
        Returns:
            status of code updation process from code request portal
        """
        codeIssueTime = dt.datetime.now()
        updateCodeRequestPayload = {
            "codeReqId": codeReqId,
            "isApproved": isApproved,
            "code": code,
            "codeIssueTime": dt.datetime.strftime(codeIssueTime, '%Y-%m-%d')
        }
        res = requests.post(self.UpdateCodeRequestApiUrl,
                            params=updateCodeRequestPayload, verify=False, auth=('903ad724-6136-4e51-bb17-d7a654b598f2', ''))
        data= res.json()
        # print(data)
        
        return data
