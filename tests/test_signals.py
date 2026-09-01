import statistics

import pytest

from src.collector import Collector

# VehicleStatus 규격 주기 (ms)
EXPECTED_CYCLE_MS = 100
# 주기 허용 오차 (ms)
CYCLE_TOLERANCE_MS = 20
# 수집 시간 (초)
COLLECT_DURATION = 3.0


@pytest.fixture(scope="module")
def frames():
    collector = Collector()
    return collector.collect(COLLECT_DURATION)


@pytest.fixture(scope="module")
def collector():
    return Collector()


def vehicle_status(frames):
    return [f for f in frames if f.name == "VehicleStatus"]


def test_message_received(frames):
    # VehicleStatus 메시지가 수신되어야 함
    assert vehicle_status(frames), "VehicleStatus 미수신"


def test_cycle_time(frames):
    # 송신 주기가 규격 범위 내여야 함
    if not vehicle_status(frames):
        pytest.skip("프레임 미수신으로 검증 불가")
    targets = vehicle_status(frames)
    intervals = [
        (b.timestamp - a.timestamp) * 1000
        for a, b in zip(targets, targets[1:])
    ]
    avg = statistics.mean(intervals)
    assert abs(avg - EXPECTED_CYCLE_MS) <= CYCLE_TOLERANCE_MS, (
        f"평균 주기 {avg:.1f}ms 가 규격 {EXPECTED_CYCLE_MS}±{CYCLE_TOLERANCE_MS}ms 이탈"
    )


@pytest.mark.parametrize(
    "signal_name",
    ["VehicleSpeed", "EngineRPM", "GearPosition", "AliveCounter"],
)
def test_signal_range(frames, collector, signal_name):
    # 모든 신호 값이 DBC 정의 범위 내여야 함
    if not vehicle_status(frames):
        pytest.skip("프레임 미수신으로 검증 불가")
    low, high = collector.signal_spec("VehicleStatus", signal_name)
    for frame in vehicle_status(frames):
        value = frame.signals[signal_name]
        assert low <= value <= high, (
            f"{signal_name}={value} 가 규격 범위 [{low}, {high}] 이탈"
        )


def test_alive_counter_increments(frames):
    # 롤링 카운터가 매 프레임 1씩 증가해야 함
    if not vehicle_status(frames):
        pytest.skip("프레임 미수신으로 검증 불가")
    values = [f.signals["AliveCounter"] for f in vehicle_status(frames)]
    for prev, curr in zip(values, values[1:]):
        expected = (prev + 1) % 16
        assert curr == expected, (
            f"롤링 카운터 불연속: {prev} 다음 {expected} 기대했으나 {curr}"
        )
