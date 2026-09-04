import time

import requests

# 대시보드 상태 조회 주소
STATE_URL = "http://127.0.0.1:5000/state"


class IviClient:
    def __init__(self, url: str = STATE_URL):
        self.url = url

    def read_state(self, timeout: float = 2.0) -> dict:
        # IVI가 현재 표시 중인 신호 값 조회
        response = requests.get(self.url, timeout=timeout)
        response.raise_for_status()
        return response.json()

    def wait_until(self, key: str, value, timeout: float = 5.0) -> bool:
        # 지정 신호가 목표 값에 도달할 때까지 대기
        deadline = time.time() + timeout
        while time.time() < deadline:
            if self.read_state().get(key) == value:
                return True
            time.sleep(0.1)
        return False
