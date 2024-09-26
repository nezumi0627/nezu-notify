from pydantic import BaseModel


class Group(BaseModel):
    mid: str
    name: str
    pictureUrl: str
