import cantools

DBC_PATH = "dbc/vehicle.dbc"


def main():
    db = cantools.database.load_file(DBC_PATH)
    for msg in db.messages:
        print(f"{msg.name} (ID=0x{msg.frame_id:X}, DLC={msg.length})")
        for sig in msg.signals:
            unit = sig.unit or ""
            print(
                f"  {sig.name}: start={sig.start} len={sig.length} "
                f"scale={sig.scale} range=[{sig.minimum}, {sig.maximum}] {unit}"
            )
        print()


if __name__ == "__main__":
    main()
