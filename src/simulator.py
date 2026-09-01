import argparse
import time

import can
import cantools

# DBC 경로
DBC_PATH = "dbc/vehicle.dbc"
# 송신 주기 (초)
CYCLE_TIME = 0.1
# 결함 모드에서 적용할 지연 주기 (초)
FAULTY_CYCLE_TIME = 0.3


def build_signals(kph: int, counter: int, fault: str) -> dict:
    # 기본 정상 신호
    signals = {
        "VehicleSpeed": kph,
        "EngineRPM": 800 + kph * 20,
        "GearPosition": 4 if kph > 0 else 0,
        "AliveCounter": counter,
        "Checksum": 0,
    }
    # 롤링 카운터 고정 결함
    if fault == "counter_stuck":
        signals["AliveCounter"] = 3
    # 신호 범위 초과 결함
    if fault == "range_over":
        signals["EngineRPM"] = 9000
    return signals


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--fault",
        default="none",
        choices=["none", "counter_stuck", "range_over", "slow_cycle", "silent"],
        help="주입할 결함 유형",
    )
    args = parser.parse_args()

    # 무전송 결함은 아무것도 보내지 않음
    if args.fault == "silent":
        print("결함 주입: 메시지 미전송 상태 유지")
        while True:
            time.sleep(1)

    cycle = FAULTY_CYCLE_TIME if args.fault == "slow_cycle" else CYCLE_TIME

    db = cantools.database.load_file(DBC_PATH)
    msg_def = db.get_message_by_name("VehicleStatus")

    counter = 0
    print(f"송신 시작 (결함={args.fault}, 주기={cycle * 1000:.0f}ms)")
    with can.Bus(channel="vcan0", interface="socketcan") as bus:
        while True:
            for kph in range(0, 121, 5):
                signals = build_signals(kph, counter, args.fault)
                # 범위 초과 값도 그대로 인코딩 (결함 재현 목적)
                data = msg_def.encode(signals, strict=False)
                bus.send(
                    can.Message(
                        arbitration_id=msg_def.frame_id,
                        data=data,
                        is_extended_id=False,
                    )
                )
                counter = (counter + 1) % 16
                time.sleep(cycle)


if __name__ == "__main__":
    main()
