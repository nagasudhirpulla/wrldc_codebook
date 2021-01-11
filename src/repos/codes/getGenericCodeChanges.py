from typing import Optional, List, Tuple, Any
from src.typeDefs.code import ICode
import datetime as dt


def getGenericCodeChanges(code: ICode, code_issue_time: Optional[dt.datetime],
                          code_str: str, other_ldc_codes: str,
                          code_description: str, code_execution_time: dt.datetime,
                          code_tags: str, code_issued_by: str, code_issued_to: str, is_code_cancelled: bool) -> List[Tuple[str, Any]]:
    """this function returns what info is changed wrt code object

    Args:
        code (ICode): [description]
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
        List[Tuple[str, Any]]: [description]
    """                          
    changedInfo: List[Tuple[str, Any]] = []

    # check if codeIssueTime has changed
    if not code["codeIssueTime"] == code_issue_time:
        changedInfo.append(("code_issue_time", code_issue_time))

    # check if code_str has changed
    if not code["codeStr"] == code_str:
        changedInfo.append(("code_str", code_str))

    # check if other ldc codes has changed
    if not code["otherLdcCodes"] == other_ldc_codes:
        changedInfo.append(("other_ldc_codes", other_ldc_codes))

    # check if code issued to has changed
    if not code["codeIssuedTo"] == code_issued_to:
        changedInfo.append(("code_issued_to", code_issued_to))

    # check if code Description has changed
    if not code["codeDesc"] == code_description:
        changedInfo.append(("code_description", code_description))

    # check if code execution time has changed
    if not code["codeExecTime"] == code_execution_time:
        changedInfo.append(("code_execution_time", code_execution_time))

    # check if code issued by has changed
    if not code["codeIssuedBy"] == code_issued_by:
        changedInfo.append(("code_issued_by", code_issued_by))

    # check if code tags has changed
    if not code["codeTags"] == code_tags:
        changedInfo.append(("code_tags", code_tags))

    # check if is code cancelled has changed
    originalCodeCancelFlag = False if code["isCodeCancelled"] == 0 else True
    if not originalCodeCancelFlag == is_code_cancelled:
        changedInfo.append(("is_code_cancelled", is_code_cancelled))

    return changedInfo
