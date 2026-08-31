import time
from dataclasses import dataclass

import can
import cantools

DBC_PATH = "dbc/vehicle.dbc"


@dataclass
class Frame:
    # 수신 시각
    timestamp: float
    # 메시지 이름
    name: str
    # 디코딩된 신호 값
    signals: dict


class Collector:
    def __init__(self, dbc_path: str = DBC_PATH, channel: str = "vcan0"):
        self.db = cantools.database.load_file(dbc_path)
        self.channel = channel

    def collect(self, duration: float) -> list[Frame]:
        # 지정 시간 동안 버스를 수신해 디코딩된 프레임 목록 반환
        frames = []
        deadline = time.time() + duration
        with can.Bus(channel=self.channel, interface="socketcan") as bus:
            while time.time() < deadline:
                msg = bus.recv(timeout=0.5)
                if msg is None:
                    continue
                try:
                    msg_def = self.db.get_message_by_frame_id(msg.arbitration_id)
                except KeyError:
                    continue
                frames.append(
                    Frame(
                        timestamp=msg.timestamp,
                        name=msg_def.name,
                        signals=msg_def.decode(msg.data),
                    )
                )
        return frames

    def signal_spec(self, msg_name: str, sig_name: str):
        # DBC에서 신호의 유효 범위를 조회
        msg_def = self.db.get_message_by_name(msg_name)
        sig = msg_def.get_signal_by_name(sig_name)
        return sig.minimum, sig.maximum
