import requests
import datetime as dt
from flask import jsonify
from src.typeDefs.getCodeRequestResp import IGetCodeRequestResp


class CodeRequestApiHandler():
    CodeRequestApiUrl = ''

    def __init__(self, CodeRequestApiUrl):
        self.CodeRequestApiUrl = CodeRequestApiUrl

    def getCodeRequest(self, startDate: dt.datetime, endDate: dt.datetime) -> IGetCodeRequestResp:
        """get code request using the api service
        Args:
            startDate (dt.datetime): start date
            endDate (dt.datetime): end date
        Returns:
            Code Request
        """
        createCodeRequestPayload = {
            "startDt": dt.datetime.strftime(startDate, '%Y-%m-%d'),
            "endDt": dt.datetime.strftime(endDate, '%Y-%m-%d')
        }
        res = requests.get(self.CodeRequestApiUrl,
                            params=createCodeRequestPayload, verify=False, auth=('903ad724-6136-4e51-bb17-d7a654b598f2', ''))

        outages= res.json()
        # print(outages)
        data=jsonify({"outages": outages})

        return data
