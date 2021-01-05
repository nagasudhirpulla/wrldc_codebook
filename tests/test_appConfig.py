import unittest
from src.appConfig import getConfig


class TestAppConfig(unittest.TestCase):
    def test_run(self) -> None:
        """tests the function that gets the application config
        """
        appConf = getConfig()
        self.assertTrue("pwcDbConnStr" in appConf)