from typing import Dict
import json
from pathlib import Path
import os
from dataclasses import dataclass

HOME_DIRECTORY = Path(os.path.expanduser("~"))


@dataclass
class Config:
    roomid: str
    cardid_to_memberid: Dict[str, str]
    presentText: str
    absentText: str


def load_config(fp: Path = HOME_DIRECTORY / "pasoruca.json") -> Config:
    with open(fp, "r") as file:
        data = json.load(file)
    return Config(
        roomid=str(data["roomId"]),
        cardid_to_memberid={
            str(cardid): str(memberid)
            for cardid, memberid in data["cardidToMemberid"].items()
        },
        presentText=data["statuses"]["presentText"],
        absentText=data["statuses"]["absentText"],
    )
