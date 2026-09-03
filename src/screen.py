import os
import subprocess

from PIL import Image

# 캡처 저장 경로
CAPTURE_DIR = "reports/captures"


class ScreenCapture:
    def __init__(self, region: tuple | None = None):
        # region: (left, top, right, bottom). None이면 전체 화면
        self.region = region

    def capture(self, name: str) -> str:
        # 전체 화면을 캡처한 뒤 지정 영역만 잘라 저장
        os.makedirs(CAPTURE_DIR, exist_ok=True)
        path = os.path.join(CAPTURE_DIR, f"{name}.png")
        subprocess.run(["gnome-screenshot", "-f", path], check=True)
        if self.region:
            img = Image.open(path)
            img.crop(self.region).save(path)
        return path

    def close(self):
        pass


def main():
    cap = ScreenCapture()
    path = cap.capture("test")
    print(f"캡처 완료: {path}")


if __name__ == "__main__":
    main()
