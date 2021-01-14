from typing import Optional, List, Tuple, Any
from src.typeDefs.code import ICode
import datetime as dt


def getElementOutageCodeChanges(code: ICode, pwc_outage_type_id: int,
                                pwc_outage_tag_id: int,
                                pwc_outage_type: str, pwc_outage_tag: str) -> List[Tuple[str, Any]]:
    """this function returns what info is changed wrt code object

    Args:
        code (ICode): [description]
        pwc_outage_type_id (int): [description]
        pwc_outage_tag_id (int): [description]
        pwc_outage_type (str): [description]
        pwc_outage_tag (str): [description]

    Returns:
        List[Tuple[str, Any]]: [description]
    """    
    changedInfo: List[Tuple[str, Any]] = []

    # check if pwcOutageTypeId has changed
    if not code["pwcOutageTypeId"] == pwc_outage_type_id:
        changedInfo.append(("pwc_outage_type_id", pwc_outage_type_id))

    # check if pwcOutageType has changed
    if not code["pwcOutageType"] == pwc_outage_type:
        changedInfo.append(("pwc_outage_type", pwc_outage_type))

    # check if pwcOutageTagId has changed
    if not code["pwcOutageTagId"] == pwc_outage_tag_id:
        changedInfo.append(("pwc_outage_tag_id", pwc_outage_tag_id))

    # check if code issued to has changed
    if not code["pwcOutageTag"] == pwc_outage_tag:
        changedInfo.append(("pwc_outage_tag", pwc_outage_tag))

    return changedInfo
