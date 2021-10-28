from typing import List, Optional
from src.repos.codeTags.deleteCodeTag import deleteCodeTag
from src.repos.codeTags.getAllCodeTags import getAllCodeTags
from src.repos.codeTags.getCodeTagById import getCodeTagById
from src.repos.codeTags.insertCodeTag import insertCodeTag
from src.typeDefs.codeTag import ICodeTag


class CodeTagsRepo():
    """Repository class for Code tags data of application
    """
    appDbConnStr: str = ""

    def __init__(self, dbConStr: str) -> None:
        """constructor method
        Args:
            dbConStr (str): database connection string
        """
        self.appDbConnStr = dbConStr

    def getAllCodeTags(self) -> List[ICodeTag]:
        """fetches all code tags
        """
        return getAllCodeTags(self.appDbConnStr)

    def getCodeTagById(self, codeTagId: int) -> Optional[ICodeTag]:
        """fetches code tag by id
        """
        return getCodeTagById(self.appDbConnStr, codeTagId)

    def deleteCodeTag(self, codeTagId: int) -> Optional[ICodeTag]:
        """deletes code tag by id
        """
        return deleteCodeTag(self.appDbConnStr, codeTagId)

    def insertCodeTag(self, codeTag: int) -> bool:
        """inserts code tag
        """
        return insertCodeTag(self.appDbConnStr, codeTag)
