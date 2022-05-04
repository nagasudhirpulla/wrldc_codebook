from typing import TypedDict


class IGetCodeRequestResp(TypedDict):
    isSuccess: bool
    status: int
    message: str