import cx_Oracle
import datetime as dt
from src.repos.codes.insertGenericCode import insertGenericCode


class CodesRepo():
    """Repository class for Codes data of application
    """
    appDbConnStr: str = ""

    def __init__(self, dbConStr: str) -> None:
        """constructor method
        Args:
            dbConStr (str): database connection string
        """
        self.appDbConnStr = dbConStr

    def insertGenericCode(self, code_issue_time: dt.datetime,
                          code_str: str, other_ldc_codes: str,
                          code_description: str, code_execution_time: dt.datetime,
                          code_tags: str, code_issued_by: str, code_issued_to: str) -> bool:
        """inserts a generic code into the app db
        Returns:
            bool: returns true if process is ok
        """
        isInsertSuccess = insertGenericCode(self.appDbConnStr, code_issue_time,
                                            code_str, other_ldc_codes,
                                            code_description, code_execution_time,
                                            code_tags, code_issued_by, code_issued_to)
        return isInsertSuccess

    def getCodes(self, startDate: dt.datetime, endDate: dt.datetime):
        fetchSql = """
            select (ID, CODE_TYPE, CODE_ISSUE_TIME, CODE_STR, OTHER_LDC_CODES, 
            CODE_DESCRIPTION, CODE_EXECUTION_TIME, CODE_TAGS, CODE_ISSUED_BY, 
            IS_CODE_CANCELLED, PWC_SD_REQ_ID, PWC_RTO_ID, IS_DELETED_AT_SRC, 
            PWC_ELEMENT_ID, PWC_ELEMENT_TYPE_ID, PWC_OUTAGE_TYPE_ID, 
            PWC_ELEMENT_NAME, PWC_ELEMENT_TYPE, PWC_OUTAGE_TYPE, CREATED_AT, 
            UPDATED_AT, CODE_ISSUED_TO) from code_book.op_codes where is_deleted=0 
            and code_issue_time between :1 and :2 order by code_issue_time desc
        """
        targetColumns = ['ID', ' CODE_TYPE', ' CODE_ISSUE_TIME', ' CODE_STR', ' OTHER_LDC_CODES',
                         'CODE_DESCRIPTION', ' CODE_EXECUTION_TIME', ' CODE_TAGS', ' CODE_ISSUED_BY',
                         'IS_CODE_CANCELLED', ' PWC_SD_REQ_ID', ' PWC_RTO_ID', ' IS_DELETED_AT_SRC',
                         'PWC_ELEMENT_ID', ' PWC_ELEMENT_TYPE_ID', ' PWC_OUTAGE_TYPE_ID',
                         'PWC_ELEMENT_NAME', ' PWC_ELEMENT_TYPE', ' PWC_OUTAGE_TYPE', ' CREATED_AT',
                         'UPDATED_AT', ' CODE_ISSUED_TO']
