import time

import can

# 차속 메시지 ID
MSG_ID_VEHICLE_SPEED = 0x100
# 송신 주기 (초)
CYCLE_TIME = 0.5


def encode_speed(kph: float) -> bytes:
    # 0.1 km/h 단위 2바이트로 인코딩
    raw = int(kph / 0.1)
    return bytes([(raw >> 8) & 0xFF, raw & 0xFF, 0, 0, 0, 0, 0, 0])


def main():
    with can.Bus(channel="vcan0", interface="socketcan") as bus:
        for kph in range(0, 121, 10):
            msg = can.Message(
                arbitration_id=MSG_ID_VEHICLE_SPEED,
                data=encode_speed(kph),
                is_extended_id=False,
            )
            bus.send(msg)
            print(f"송신 차속={kph} km/h")
            time.sleep(CYCLE_TIME)


if __name__ == "__main__":
    main()
