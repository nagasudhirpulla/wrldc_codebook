import unittest
from src.appConfig import initAppConfig


class TestAppConfig(unittest.TestCase):
    def test_run(self) -> None:
        """tests the function that gets the application config
        """
        appConf = initAppConfig()
        self.assertTrue("pwcDbConnStr" in appConf)
        self.assertTrue("appDbConnStr" in appConf)
