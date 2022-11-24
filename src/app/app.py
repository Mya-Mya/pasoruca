from typing import Dict
import json
from pathlib import Path
import os
from dataclasses import dataclass

HOME_DIRECTORY = Path(os.path.expanduser("~"))


@dataclass
class Config:
    room_code: str
    cardid_to_memberid: Dict[str, str]
    presentText: str
    absentText: str


def load_config(fp: Path = HOME_DIRECTORY / "pasoruca.json") -> Config:
    with open(fp, "r") as file:
        data = json.load(file)
    config = Config(
        room_code=str(data["roomCode"]),
        cardid_to_memberid={
            str(cardid): str(memberid)
            for cardid, memberid in data["cardidToMemberid"].items()
        },
        presentText=data["statuses"]["presentText"],
        absentText=data["statuses"]["absentText"],
    )
    return config
