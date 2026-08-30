import can


def main():
    # vcan0 버스에 연결
    with can.Bus(channel="vcan0", interface="socketcan") as bus:
        print("수신 대기 중. Ctrl+C 로 종료")
        # 버스를 순회하며 프레임 수신
        for msg in bus:
            frame_id = f"0x{msg.arbitration_id:03X}"
            payload = msg.data.hex(" ").upper()
            print(f"[{msg.timestamp:.3f}] ID={frame_id} DLC={msg.dlc} DATA={payload}")


if __name__ == "__main__":
    main()

