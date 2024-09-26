from pydantic import BaseModel


class IssueTokenResponse(BaseModel):
    token: str
