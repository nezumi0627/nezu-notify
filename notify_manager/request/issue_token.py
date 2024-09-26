from typing import Any, Self

from pydantic import BaseModel

from notify_manager.models.group import Group


class IssueTokenRequest(BaseModel):
    description: str
    targetType: str
    targetMid: str
    csrf: str
    action: str = "issuePersonalAcessToken"

    @property
    def data(self) -> dict[str, Any]:
        d = self.model_dump()
        d["_csrf"] = d.pop("csrf")
        return d  # type: ignore [no-any-return]

    @classmethod
    def by_user(cls, description: str, csrf_token: str) -> Self:
        return cls(
            description=description,
            csrf=csrf_token,
            targetType="USER",
            targetMid="USER",
        )

    @classmethod
    def by_group(cls, group: Group, description: str, csrf_token: str) -> Self:
        return cls(
            description=description,
            csrf=csrf_token,
            targetType="GROUP",
            targetMid=group.mid,
        )
