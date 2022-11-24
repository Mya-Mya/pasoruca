from typing import Dict
from dataclasses import dataclass


@dataclass
class Config:
    roomid: str
    cardid_to_memberid: Dict[str, str]
    presentText: str
    absentText: str


