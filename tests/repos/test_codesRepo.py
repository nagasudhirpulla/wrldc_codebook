import unittest
from src.appConfig import getConfig
from src.repos.codes.codesRepo import CodesRepo
import datetime as dt


class TestCodesRepo(unittest.TestCase):
    def setUp(self):
        self.appConf = getConfig()

    def test_insertGenericCode(self) -> None:
        """tests the function that gets the application config
        """
        appDbConnStr = self.appConf['appDbConnStr']
        cRepo = CodesRepo(appDbConnStr)
        # no execution time
        isSuccess = cRepo.insertGenericCode(
            code_issue_time=None, code_str="TEST_01", other_ldc_codes=None,
            code_description="test description", code_execution_time=None,
            code_tags="TESTING", code_issued_by="NA", code_issued_to="NA")
        self.assertTrue(isSuccess)
        # with execution time
        isSuccess = cRepo.insertGenericCode(
            code_issue_time=None, code_str="TEST_01", other_ldc_codes=None,
            code_description="test description", code_execution_time=dt.datetime.now(),
            code_tags="TESTING", code_issued_by="NA", code_issued_to="NA")
        self.assertTrue(isSuccess)
