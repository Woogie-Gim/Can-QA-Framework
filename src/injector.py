import can
import cantools

DBC_PATH = "dbc/vehicle.dbc"


class Injector:
    def __init__(self, channel: str = "vcan0"):
        self.db = cantools.database.load_file(DBC_PATH)
        self.bus = can.Bus(channel=channel, interface="socketcan")
        self.counter = 0

    def send_status(self, speed: int, rpm: int = 800, gear: int = 4):
        # VehicleStatus 메시지를 지정 값으로 송신
        msg_def = self.db.get_message_by_name("VehicleStatus")
        data = msg_def.encode(
            {
                "VehicleSpeed": speed,
                "EngineRPM": rpm,
                "GearPosition": gear,
                "AliveCounter": self.counter,
                "Checksum": 0,
            },
            strict=False,
        )
        self.counter = (self.counter + 1) % 16
        self._send(msg_def.frame_id, data)

    def send_door(self, driver_open: int = 0):
        # DoorStatus 메시지 송신
        msg_def = self.db.get_message_by_name("DoorStatus")
        data = msg_def.encode(
            {
                "DriverDoorOpen": driver_open,
                "PassengerDoorOpen": 0,
                "TrunkOpen": 0,
            }
        )
        self._send(msg_def.frame_id, data)

    def _send(self, frame_id: int, data: bytes):
        self.bus.send(
            can.Message(
                arbitration_id=frame_id,
                data=data,
                is_extended_id=False,
            )
        )

    def close(self):
        self.bus.shutdown()
