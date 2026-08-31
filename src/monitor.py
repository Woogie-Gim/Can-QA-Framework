import can
import cantools

DBC_PATH = "dbc/vehicle.dbc"


def main():
    db = cantools.database.load_file(DBC_PATH)

    with can.Bus(channel="vcan0", interface="socketcan") as bus:
        print("수신 대기 중. Ctrl+C 로 종료")
        for msg in bus:
            try:
                decoded = db.decode_message(msg.arbitration_id, msg.data)
            except KeyError:
                # DBC에 정의되지 않은 ID는 건너뜀
                continue
            name = db.get_message_by_frame_id(msg.arbitration_id).name
            print(f"[{msg.timestamp:.3f}] {name} {decoded}")


if __name__ == "__main__":
    main()
