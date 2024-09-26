from pydantic import BaseModel

from notify_manager.models.group import Group


class GetGroupListResponse(BaseModel):
    status: int
    results: list[Group]
