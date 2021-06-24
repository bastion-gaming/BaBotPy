from typing import List, Optional
from pydantic import BaseModel


class TableComTime(BaseModel):
    playerid: int
    command: str
    time: str = None

    class Config:
        orm_mode = True


class TableCoreOld(BaseModel):
    playerid: int
    discord_id: str
    level: int
    xp: int

    class Config:
        orm_mode = True



class TableCore(BaseModel):
    playerid: int
    discord_id: str
    arrival: str
    level: int
    xp: int
    devise: int
    super_devise: int
    godparent: int
    nbreaction: int
    nbmsg: int
    com_time: List[TableComTime] = []

    class Config:
        orm_mode = True
