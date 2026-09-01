import subprocess
import sys
import time

# 순회할 결함 조건
FAULTS = ["none", "counter_stuck", "range_over", "slow_cycle", "silent"]
# 시뮬레이터 기동 대기 시간 (초)
STARTUP_WAIT = 1.0


def run_case(fault: str) -> int:
    print(f"\n{'=' * 60}")
    print(f"검증 조건: {fault}")
    print(f"{'=' * 60}")

    # 시뮬레이터를 백그라운드로 기동
    sim = subprocess.Popen(
        [sys.executable, "src/simulator.py", "--fault", fault],
        stdout=subprocess.DEVNULL,
    )
    time.sleep(STARTUP_WAIT)

    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "-v", "--fault", fault]
        )
        return result.returncode
    finally:
        # 조건별 검증 후 반드시 시뮬레이터 종료
        sim.terminate()
        sim.wait()


def main():
    for fault in FAULTS:
        run_case(fault)
    print("\n전체 조건 검증 완료. reports/ 폴더를 확인하세요.")


if __name__ == "__main__":
    main()
