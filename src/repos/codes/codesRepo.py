import datetime as dt
from src.repos.codes.insertGenericCode import insertGenericCode
from src.repos.codes.insertElementCode import insertElementCode
from src.repos.codes.insertElementOutageCode import insertElementOutageCode
from src.repos.codes.editGenericCode import editGenericCode
from src.repos.codes.editElementCode import editElementCode
from src.repos.codes.editElementOutageCode import editElementOutageCode
from src.repos.codes.getCodesBetweenDates import getCodesBetweenDates
from src.repos.codes.getCodeById import getCodeById
from src.repos.codes.deleteCode import deleteCode
from typing import List, Optional
from src.typeDefs.code import ICode


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

    def getCodesBetweenDates(self, startDt: dt.datetime, endDt: dt.datetime) -> List[ICode]:
        """fetches codes between 2 dates from app db

        Args:
            startDt (dt.datetime): [description]
            endDt (dt.datetime): [description]

        Returns:
            List[ICode]: list of code objects
        """
        return getCodesBetweenDates(self.appDbConnStr, startDt, endDt)

    def getCodeById(self, codeId: int) -> Optional[ICode]:
        """fetches code object by id

        Args:
            codeId (int): [description]

        Returns:
            Optional[ICode]: code object
        """
        return getCodeById(self.appDbConnStr, codeId)

    def deleteCode(self, codeId: int) -> bool:
        """delete a code with id

        Args:
            codeId (int): [description]
        Returns:
            bool: returns true if code is deleted successfully
        """
        return deleteCode(self.appDbConnStr, codeId)

    def editGenericCode(self, codeId: int, code_issue_time: Optional[dt.datetime],
                        code_str: str, other_ldc_codes: str,
                        code_description: str, code_execution_time: dt.datetime,
                        code_tags: str, code_issued_by: str, code_issued_to: str, is_code_cancelled: bool) -> bool:
        """edit a generic code

        Args:
            codeId (int): [description]
            code_issue_time (Optional[dt.datetime]): [description]
            code_str (str): [description]
            other_ldc_codes (str): [description]
            code_description (str): [description]
            code_execution_time (dt.datetime): [description]
            code_tags (str): [description]
            code_issued_by (str): [description]
            code_issued_to (str): [description]
            is_code_cancelled (bool): [description]

        Returns:
            bool: return true if edit is success
        """
        return editGenericCode(self.appDbConnStr, codeId, code_issue_time,
                               code_str, other_ldc_codes,
                               code_description, code_execution_time,
                               code_tags, code_issued_by, code_issued_to, is_code_cancelled)

    def insertElementCode(self, code_issue_time: dt.datetime,
                          code_str: str, other_ldc_codes: str,
                          code_description: str, code_execution_time: dt.datetime,
                          code_tags: str, code_issued_by: str, code_issued_to: str,
                          pwc_element_type_id: int, pwc_element_id: int,
                          pwc_element_name: str, pwc_element_type: str) -> bool:
        """inserts an element code into the app db
        Returns:
            bool: returns true if process is ok
        """
        isInsertSuccess = insertElementCode(self.appDbConnStr, code_issue_time,
                                            code_str, other_ldc_codes,
                                            code_description, code_execution_time,
                                            code_tags, code_issued_by, code_issued_to,
                                            pwc_element_type_id, pwc_element_id,
                                            pwc_element_name, pwc_element_type)
        return isInsertSuccess

    def editElementCode(self, codeId: int, code_issue_time: Optional[dt.datetime],
                        code_str: str, other_ldc_codes: str,
                        code_description: str, code_execution_time: dt.datetime,
                        code_tags: str, code_issued_by: str, code_issued_to: str, is_code_cancelled: bool) -> bool:
        """edit as element code

        Args:
            codeId (int): [description]
            code_issue_time (Optional[dt.datetime]): [description]
            code_str (str): [description]
            other_ldc_codes (str): [description]
            code_description (str): [description]
            code_execution_time (dt.datetime): [description]
            code_tags (str): [description]
            code_issued_by (str): [description]
            code_issued_to (str): [description]
            is_code_cancelled (bool): [description]

        Returns:
            bool: return true if edit is success
        """
        return editElementCode(self.appDbConnStr, codeId, code_issue_time,
                               code_str, other_ldc_codes,
                               code_description, code_execution_time,
                               code_tags, code_issued_by, code_issued_to, is_code_cancelled)

    def insertElementOutageCode(self, code_issue_time: Optional[dt.datetime],
                                code_str: str, other_ldc_codes: str,
                                code_description: str, code_execution_time: dt.datetime,
                                code_tags: str, code_issued_by: str, code_issued_to: str,
                                pwc_element_type_id: int, pwc_element_id: int,
                                pwc_element_name: str, pwc_element_type: str,
                                pwc_outage_type_id: int, pwc_outage_tag_id: int,
                                pwc_outage_type: str, pwc_outage_tag: str) -> bool:
        """inserts an element outage code into the app db
        Returns:
            bool: returns true if process is ok
        """
        isInsertSuccess = insertElementOutageCode(self.appDbConnStr, code_issue_time,
                                                  code_str, other_ldc_codes,
                                                  code_description, code_execution_time,
                                                  code_tags, code_issued_by, code_issued_to,
                                                  pwc_element_type_id, pwc_element_id,
                                                  pwc_element_name, pwc_element_type,
                                                  pwc_outage_type_id, pwc_outage_tag_id,
                                                  pwc_outage_type, pwc_outage_tag)
        return isInsertSuccess

    def editElementOutageCode(self, codeId: int, code_issue_time: Optional[dt.datetime],
                              code_str: str, other_ldc_codes: str,
                              code_description: str, code_execution_time: dt.datetime,
                              code_tags: str, code_issued_by: str, code_issued_to: str,
                              is_code_cancelled: bool, pwc_outage_type_id: int,
                              pwc_outage_tag_id: int, pwc_outage_type: str,
                              pwc_outage_tag: str) -> bool:
        """edit element outage code

        Args:
            codeId (int): [description]
            code_issue_time (Optional[dt.datetime]): [description]
            code_str (str): [description]
            other_ldc_codes (str): [description]
            code_description (str): [description]
            code_execution_time (dt.datetime): [description]
            code_tags (str): [description]
            code_issued_by (str): [description]
            code_issued_to (str): [description]
            is_code_cancelled (bool): [description]
            pwc_outage_type_id (int): [description]
            pwc_outage_tag_id (int): [description]
            pwc_outage_type (str): [description]
            pwc_outage_tag (str): [description]

        Returns:
            bool: returns true if element outage code editing is ok
        """
        return editElementOutageCode(self.appDbConnStr, codeId, code_issue_time,
                                     code_str, other_ldc_codes,
                                     code_description, code_execution_time,
                                     code_tags, code_issued_by, code_issued_to,
                                     is_code_cancelled, pwc_outage_type_id,
                                     pwc_outage_tag_id, pwc_outage_type,
                                     pwc_outage_tag)
