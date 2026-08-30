#!/bin/bash
# vcan0 생성 및 활성화
sudo modprobe vcan
sudo ip link add dev vcan0 type vcan 2>/dev/null
sudo ip link set up vcan0
ip -brief link show vcan0
