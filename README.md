# CAN QA Framework

DBC 기반 CAN 신호 검증 자동화 프레임워크

## 개요

차량 내 ECU 간 통신에 사용되는 CAN 프로토콜의 신호 정합성을 자동으로 검증하는 테스트 프레임워크. 실제 차량 하드웨어 없이 가상 CAN 인터페이스 위에서 ECU를 시뮬레이션하고 DBC 명세를 기준으로 신호를 검증한다.

## 개발 환경

| 항목 | 내용 |
|---|---|
| OS | Ubuntu 26.04 LTS (VirtualBox) |
| 인터페이스 | SocketCAN (vcan0) |
| 언어 | Python 3 |
| 주요 라이브러리 | python-can, cantools, pytest, openpyxl |

## 실행 방법

가상 CAN 인터페이스 활성화

```bash
./scripts/setup_vcan.sh
```

가상환경 활성화 및 의존성 설치

```bash
source venv/bin/activate
pip install -r requirements.txt
```

송수신 확인

```bash
# 터미널 1
python src/monitor.py

# 터미널 2
python src/simulator.py
```

## 프로젝트 구조
can-qa-framework/
├── src/ # 시뮬레이터 및 모니터
├── dbc/ # CAN 신호 명세
├── tests/ # pytest 테스트 케이스
├── reports/ # 검증 결과 리포트
└── scripts/ # 환경 구성 스크립트

## 진행 현황

- [x] 가상 CAN 환경 구축 및 송수신 검증
- [ ] DBC 명세 작성 및 신호 인코딩/디코딩
- [ ] 가상 ECU 시뮬레이터 및 결함 주입
- [ ] 신호 검증 테스트 케이스
- [ ] 검증 결과 리포트 생성
