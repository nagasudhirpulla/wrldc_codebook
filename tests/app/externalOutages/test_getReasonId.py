import unittest
from src.appConfig import initAppConfig
from src.app.externalOutages.getReasonId import getReasonId


class TestGetReasonId(unittest.TestCase):
    def test_run(self) -> None:
        """tests the function that gets the reason Id
        """
        appConf = initAppConfig()
        reasId = getReasonId(appConf["pwcDbConnStr"], "VR", 4)
        self.assertFalse(reasId == -1)
