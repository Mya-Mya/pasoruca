from typing import Dict
import json
from pathlib import Path
import os
from dataclasses import dataclass
import irucapy
from typing import Optional
from enum import Enum

HOME_DIRECTORY = Path(os.path.expanduser("~"))


@dataclass
class Config:
    room_code: str
    cardid_to_memberid: Dict[str, str]
    presentText: str
    absentText: str


class SwitchDirection(Enum):
    PRESENT_TO_ABSENT = 0
    ABSENT_TO_PRESENT = 1


@dataclass
class SwitchResult:
    member_id: str
    name: str
    direction: SwitchDirection


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


class App:
    def __init__(self, config_fp: Path = HOME_DIRECTORY / "pasoruca.json") -> None:
        self.config = load_config(config_fp)
        self.irucapy_client = irucapy.IrucaClient(
            room_code=self.config.room_code, api=irucapy.HTTPIrucaAPI()
        )

    def switch_status_by_cardid(self, cardid: str) -> Optional[SwitchResult]:
        if cardid in self.config.cardid_to_memberid:
            member_id = self.config.cardid_to_memberid[cardid]
        else:
            raise ValueError(f"Card id {cardid} is not registered in your config.")

        member = self.irucapy_client.get_room_member(member_id=member_id)

        switch_direction = None
        if member.status == self.config.presentText:
            switch_direction = SwitchDirection.PRESENT_TO_ABSENT
            self.irucapy_client.update_room_member(
                member_id=member_id, status=self.config.absentText
            )
        elif member.status == self.config.absentText:
            switch_direction = SwitchDirection.ABSENT_TO_PRESENT
            self.irucapy_client.update_room_member(
                member_id=member_id, status=self.config.presentText
            )
        else:
            raise ValueError(
                f"Member {member.name}'s status {member.status} is not supported in your config.\
                  Member status must be either {self.config.presentText} or {self.config.absentText}."
            )
        return SwitchResult(
            member_id=member_id, name=member.name, direction=switch_direction
        )
