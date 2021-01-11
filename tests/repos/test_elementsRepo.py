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

    def test_getBusesForDisplay(self) -> None:
        """tests the function that gets elements for display from outage software
        """
        pwcDbConnStr = self.appConf['pwcDbConnStr']
        eRepo = ElementsRepo(pwcDbConnStr)
        elems = eRepo.getBusesForDisplay()
        self.assertFalse(len(elems) == 0)

    def test_getBusReactorsForDisplay(self) -> None:
        """tests the function that gets elements for display from outage software
        """
        pwcDbConnStr = self.appConf['pwcDbConnStr']
        eRepo = ElementsRepo(pwcDbConnStr)
        elems = eRepo.getBusReactorsForDisplay()
        self.assertFalse(len(elems) == 0)

    def test_getFilterBanksForDisplay(self) -> None:
        """tests the function that gets elements for display from outage software
        """
        pwcDbConnStr = self.appConf['pwcDbConnStr']
        eRepo = ElementsRepo(pwcDbConnStr)
        elems = eRepo.getFilterBanksForDisplay()
        self.assertFalse(len(elems) == 0)

    def test_getFscsForDisplay(self) -> None:
        """tests the function that gets elements for display from outage software
        """
        pwcDbConnStr = self.appConf['pwcDbConnStr']
        eRepo = ElementsRepo(pwcDbConnStr)
        elems = eRepo.getFscsForDisplay()
        self.assertFalse(len(elems) == 0)

    def test_getGeneratingUnitsForDisplay(self) -> None:
        """tests the function that gets elements for display from outage software
        """
        pwcDbConnStr = self.appConf['pwcDbConnStr']
        eRepo = ElementsRepo(pwcDbConnStr)
        elems = eRepo.getGeneratingUnitsForDisplay()
        self.assertFalse(len(elems) == 0)
    
    def test_getHvdcLineCktsForDisplay(self) -> None:
        """tests the function that gets elements for display from outage software
        """
        pwcDbConnStr = self.appConf['pwcDbConnStr']
        eRepo = ElementsRepo(pwcDbConnStr)
        elems = eRepo.getHvdcLineCktsForDisplay()
        self.assertFalse(len(elems) == 0)
    
    def test_getHvdcPolesForDisplay(self) -> None:
        """tests the function that gets elements for display from outage software
        """
        pwcDbConnStr = self.appConf['pwcDbConnStr']
        eRepo = ElementsRepo(pwcDbConnStr)
        elems = eRepo.getHvdcPolesForDisplay()
        self.assertFalse(len(elems) == 0)
    
    def test_getSvcsForDisplay(self) -> None:
        """tests the function that gets elements for display from outage software
        """
        pwcDbConnStr = self.appConf['pwcDbConnStr']
        eRepo = ElementsRepo(pwcDbConnStr)
        elems = eRepo.getSvcsForDisplay()
        self.assertFalse(len(elems) == 0)

    def test_getTcscsForDisplay(self) -> None:
        """tests the function that gets elements for display from outage software
        """
        pwcDbConnStr = self.appConf['pwcDbConnStr']
        eRepo = ElementsRepo(pwcDbConnStr)
        elems = eRepo.getTcscsForDisplay()
        self.assertFalse(len(elems) == 0)
    
    def test_getTransformersForDisplay(self) -> None:
        """tests the function that gets elements for display from outage software
        """
        pwcDbConnStr = self.appConf['pwcDbConnStr']
        eRepo = ElementsRepo(pwcDbConnStr)
        elems = eRepo.getTransformersForDisplay()
        self.assertFalse(len(elems) == 0)