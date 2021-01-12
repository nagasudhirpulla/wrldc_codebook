import unittest
from src.appConfig import initAppConfig
from src.repos.outageTypes.outageTypesRepo import OutageTypesRepo
import datetime as dt


class TestOutageTypesRepo(unittest.TestCase):
    def setUp(self):
        self.appConf = initAppConfig()

    def test_getBaysForDisplay(self) -> None:
        """tests the function that gets elements for display from outage software
        """
        pwcDbConnStr = self.appConf['pwcDbConnStr']
        oRepo = OutageTypesRepo(pwcDbConnStr)
        oTypes = oRepo.getRealTimeOutageTypes()
        self.assertFalse(len(oTypes) == 0)