from typing import Optional

from pydantic import BaseModel


class BaseWaitResponse(BaseModel):
    redirectPath: Optional[str]
    errorCode: Optional[int]
    error: Optional[str]
