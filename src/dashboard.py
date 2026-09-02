import threading

import can
import cantools
from flask import Flask, jsonify, render_template_string

DBC_PATH = "dbc/vehicle.dbc"

app = Flask(__name__)

# 최신 수신 신호 보관
_state = {
    "VehicleSpeed": 0,
    "EngineRPM": 0,
    "GearPosition": 0,
    "DriverDoorOpen": 0,
}
_lock = threading.Lock()

PAGE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body { background:#111; color:#eee; font-family:sans-serif; margin:0; }
  .wrap { display:flex; height:100vh; }
  .left { flex:1; padding:40px; }
  .right { width:360px; padding:40px; }
  .label { font-size:18px; color:#888; }
  #speed { font-size:160px; font-weight:bold; color:#fff;
           background:#000; display:inline-block; padding:0 24px; }
  #rpm { font-size:48px; }
  #gear { font-size:64px; font-weight:bold; }
  #rearcam { width:320px; height:200px; background:#222;
             display:flex; align-items:center; justify-content:center;
             font-size:24px; color:#444; }
  #rearcam.on { background:#1e7d32; color:#fff; }
  #doorwarn { width:320px; height:80px; margin-top:20px; background:#222;
              display:flex; align-items:center; justify-content:center;
              font-size:22px; color:#444; }
  #doorwarn.on { background:#c62828; color:#fff; }
</style>
</head>
<body>
<div class="wrap">
  <div class="left">
    <div class="label">SPEED (km/h)</div>
    <div id="speed">0</div>
    <div class="label" style="margin-top:30px">RPM</div>
    <div id="rpm">0</div>
    <div class="label" style="margin-top:30px">GEAR</div>
    <div id="gear">P</div>
  </div>
  <div class="right">
    <div id="rearcam">REAR CAMERA</div>
    <div id="doorwarn">DOOR</div>
  </div>
</div>
<script>
const GEARS = {0:'P', 1:'R', 2:'N', 4:'D'};
async function refresh() {
  const r = await fetch('/state');
  const s = await r.json();
  document.getElementById('speed').textContent = Math.round(s.VehicleSpeed);
  document.getElementById('rpm').textContent = Math.round(s.EngineRPM);
  document.getElementById('gear').textContent = GEARS[s.GearPosition] || '-';
  document.getElementById('rearcam').className = s.GearPosition == 1 ? 'on' : '';
  document.getElementById('doorwarn').className = s.DriverDoorOpen == 1 ? 'on' : '';
}
setInterval(refresh, 200);
refresh();
</script>
</body>
</html>
"""


def can_listener():
    # 백그라운드에서 CAN 수신하여 상태 갱신
    db = cantools.database.load_file(DBC_PATH)
    with can.Bus(channel="vcan0", interface="socketcan") as bus:
        for msg in bus:
            try:
                msg_def = db.get_message_by_frame_id(msg.arbitration_id)
            except KeyError:
                continue
            decoded = msg_def.decode(msg.data)
            with _lock:
                for key in _state:
                    if key in decoded:
                        _state[key] = decoded[key]


@app.route("/")
def index():
    return render_template_string(PAGE)


@app.route("/state")
def state():
    with _lock:
        return jsonify(dict(_state))


def main():
    threading.Thread(target=can_listener, daemon=True).start()
    app.run(host="127.0.0.1", port=5000)


if __name__ == "__main__":
    main()
