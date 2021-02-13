import unittest
from src.appConfig import initAppConfig
from src.repos.codes.codesRepo import CodesRepo
import datetime as dt
import cx_Oracle


class TestCodesRepo(unittest.TestCase):
    def setUp(self):
        self.appConf = initAppConfig()

    def test_createGenericCode(self) -> None:
        """tests the function that gets creates generic code
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

    def test_getCodesBetweenDates(self) -> None:
        """tests the function that gets the codes
        """
        appDbConnStr = self.appConf['appDbConnStr']
        cRepo = CodesRepo(appDbConnStr)
        # no execution time
        codes = cRepo.getCodesBetweenDates(startDt=dt.datetime(
            2021, 1, 6), endDt=dt.datetime(2021, 1, 6))
        self.assertTrue(len(codes) > 0)

    def test_getLatestCode(self) -> None:
        """tests the function that gets the latest code
        """
        appDbConnStr = self.appConf['appDbConnStr']
        cRepo = CodesRepo(appDbConnStr)
        # no execution time
        code = cRepo.getLatestCode()
        self.assertFalse(code == None)

    def test_getNextCodeForInsertion(self) -> None:
        """tests the function that gets Next Code For Insertion
        """
        appDbConnStr = self.appConf['appDbConnStr']
        cRepo = CodesRepo(appDbConnStr)
        dbConn = None
        dbCur = None
        nextCode = None
        try:
            # get connection with raw data table
            dbConn = cx_Oracle.connect(appDbConnStr)

            # get cursor and execute fetch sql
            dbCur = dbConn.cursor()

            nextCode = cRepo.getNextCodeForInsertion(dbCur=dbCur)
        except Exception as err:
            print('Error while fetching next code for insertion from codes repo')
            print(err)
        finally:
            # closing database cursor and connection
            if dbCur is not None:
                dbCur.close()
            if dbConn is not None:
                dbConn.close()
        print(nextCode)
        self.assertFalse(nextCode == None)

    def test_getCodesForRtoIds(self) -> None:
        """tests the function that gets codes for rto Ids
        """
        appDbConnStr = self.appConf['appDbConnStr']
        cRepo = CodesRepo(appDbConnStr)
        rtoCodes = cRepo.getCodesForRtoIds([430, 5163])
        # print(rtoCodes)
        self.assertFalse(len(rtoCodes) == 0)
