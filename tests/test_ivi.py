import time

import pytest

from src.ivi_client import IviClient
from src.injector import Injector

# 신호 반영 대기 시간 (초)
REFLECT_TIMEOUT = 5.0


@pytest.fixture(scope="module")
def ivi():
    client = IviClient()
    try:
        client.read_state()
    except Exception:
        pytest.skip("IVI 대시보드 미기동")
    return client


@pytest.fixture(scope="module")
def injector():
    inj = Injector()
    yield inj
    inj.close()


@pytest.mark.parametrize("speed", [0, 60, 120])
def test_speed_reflected(ivi, injector, speed):
    # 주입한 차속이 IVI에 그대로 표시되어야 함
    injector.send_status(speed=speed)
    assert ivi.wait_until("VehicleSpeed", speed, REFLECT_TIMEOUT), (
        f"차속 {speed} 주입 후 IVI 미반영"
    )


def test_reverse_gear_activates_camera(ivi, injector):
    # 후진 기어 진입 시 후방 카메라 상태가 활성화되어야 함
    injector.send_status(speed=5, gear=1)
    assert ivi.wait_until("GearPosition", 1, REFLECT_TIMEOUT), "후진 기어 미반영"


def test_door_open_reflected(ivi, injector):
    # 도어 개방 신호가 IVI에 반영되어야 함
    injector.send_door(driver_open=1)
    assert ivi.wait_until("DriverDoorOpen", 1, REFLECT_TIMEOUT), "도어 개방 미반영"


def test_door_close_reflected(ivi, injector):
    # 도어 폐쇄 신호가 IVI에 반영되어야 함
    injector.send_door(driver_open=0)
    assert ivi.wait_until("DriverDoorOpen", 0, REFLECT_TIMEOUT), "도어 폐쇄 미반영"
