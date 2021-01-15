import unittest
from src.appConfig import initAppConfig
from src.repos.outages.outagesRepo import OutagesRepo
import datetime as dt


class TestOutageTypesRepo(unittest.TestCase):
    def setUp(self):
        self.appConf = initAppConfig()

    def test_getLatestUnrevOutages(self) -> None:
        """tests the function that gets elements for display from outage software
        """
        pwcDbConnStr = self.appConf['pwcDbConnStr']
        oRepo = OutagesRepo(pwcDbConnStr)
        outages = oRepo.getLatestUnrevOutages()
        self.assertFalse(len(outages) == 0)
