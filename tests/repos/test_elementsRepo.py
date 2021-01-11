import unittest
from src.appConfig import initAppConfig
from src.repos.elements.elementsRepo import ElementsRepo
import datetime as dt


class TestElementsRepo(unittest.TestCase):
    def setUp(self):
        self.appConf = initAppConfig()

    def test_getBaysForDisplay(self) -> None:
        """tests the function that gets elements for display from outage software
        """
        pwcDbConnStr = self.appConf['pwcDbConnStr']
        eRepo = ElementsRepo(pwcDbConnStr)
        bays = eRepo.getBaysForDisplay()
        self.assertFalse(len(bays) == 0)

    def test_getTransLineCktsForDisplay(self) -> None:
        """tests the function that gets elements for display from outage software
        """
        pwcDbConnStr = self.appConf['pwcDbConnStr']
        eRepo = ElementsRepo(pwcDbConnStr)
        elems = eRepo.getTranLineCktsForDisplay()
        self.assertFalse(len(elems) == 0)
