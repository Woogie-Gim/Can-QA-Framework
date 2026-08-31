import time

import can
import cantools

# DBC 경로
DBC_PATH = "dbc/vehicle.dbc"
# 송신 주기 (초)
CYCLE_TIME = 0.1


def main():
    db = cantools.database.load_file(DBC_PATH)
    msg_def = db.get_message_by_name("VehicleStatus")

    counter = 0
    with can.Bus(channel="vcan0", interface="socketcan") as bus:
        while True:
            for kph in range(0, 121, 5):
                # 신호를 이름과 실제 단위로 지정
                signals = {
                    "VehicleSpeed": kph,
                    "EngineRPM": 800 + kph * 20,
                    "GearPosition": 4 if kph > 0 else 0,
                    "AliveCounter": counter,
                    "Checksum": 0,
                }
                data = msg_def.encode(signals)
                bus.send(
                    can.Message(
                        arbitration_id=msg_def.frame_id,
                        data=data,
                        is_extended_id=False,
                    )
                )
                print(f"송신 속도={kph} RPM={signals['EngineRPM']} 카운터={counter}")
                counter = (counter + 1) % 16
                time.sleep(CYCLE_TIME)


if __name__ == "__main__":
    main()
