import modi
import time
import requests
import json
import os

class SunFollower:
    def __init__(self, network_uuid=None):
        self.uuid = network_uuid or os.getenv("MODI_NETWORK_UUID")  #환경 변수 또는 인자로 받은 값
        # 하드웨어 모듈 초기화
        if not self.uuid:
            print("경고: Network UUID가 설정되지 않았습니다. 연결에 실패할 수 있습니다.")
        
        self.bundle = modi.MODI(conn_type="ble", network_uuid=self.uuid)
        self.motor = self.bundle.motors[0]
        self.env = self.bundle.envs[0]
        self.speaker = self.bundle.speakers[0]
        self.button = self.bundle.buttons[0]
        
        self.THRESHOLD_FIND = 5    # 빛 감지 시작 최소 조도
        self.THRESHOLD_GOAL = 20   # 목적지 도달 판단 조도
        self.MOVE_SPEED = 50       # 기본 주행 속도
        self.ROTATE_SPEED = 30     # 탐색 회전 속도

    def check_weather_condition(self, city="Seoul"):
        
        api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
            print("API 키가 설정되지 않았습니다. 날씨 확인을 건너뜁니다.")
            return True
        
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&APPID={api_key}"  #Weather API
        
        try:
            response = requests.get(url, timeout=5)
            data = json.loads(response.text)
            weather = data['weather'][0]['main']
            
            if weather == "Rain":
                print(f"[{city}] 강우 감지: 로봇 보호를 위해 작동을 중지합니다.")
                return False
            print(f"[{city}] 날씨 환경 ({weather}): 주행을 시작합니다.")
            return True
        except Exception as e:
            print(f"날씨 정보 확인 불가: 기본 설정을 유지합니다. ({e})")
            return True

    def avoid_obstacles(self):
        if self.button.pressed:
            print("장애물 감지: 후진 및 방향 재설정을 시작합니다.")
            
            # 정지 및 후진
            self.motor.speed = -50, 50 
            time.sleep(2)
            
            # 일시 정지
            self.motor.speed = 0, 0
            time.sleep(1)
            
            # 방향 전환
            print("우회 경로 탐색 중")
            self.motor.speed = 50, -30
            time.sleep(3)
            
            # 일시 정지
            self.motor.speed = 0, 0
            time.sleep(1)
            
            # 방향 전환 (목적지 방향을 고려한 각도 조정)
            self.motor.speed = 30, -60
            time.sleep(3)
            
            print("장애물 회피 완료. 광원 추적을 재개합니다.")
            return True
        return False

    def drive_system(self, timeout_sec=100):
        #주행 알고리즘
        start_time = time.time()
        
        while True:
            current_brightness = self.env.brightness
            elapsed_time = time.time() - start_time

            # 시간 초과 시 정지
            if elapsed_time > timeout_sec:
                print("탐색 시간 초과: 목표를 찾지 못해 시스템을 종료합니다.")
                self.stop_robot()
                break

            # 목적지 도달 확인
            if current_brightness >= self.THRESHOLD_GOAL:
                print(f"목적지 도달 (조도: {current_brightness}): 서비스를 완료합니다.")
                self.complete_service()
                break

            # 광원 탐색 및 주행
            if current_brightness >= self.THRESHOLD_FIND:
                print(f"광원 추적 중 (현재 조도: {current_brightness})")
                self.motor.speed = self.MOVE_SPEED, -self.MOVE_SPEED # 직진
            else:
                print("주변 탐색 중 (회전)")
                self.motor.speed = self.ROTATE_SPEED, self.ROTATE_SPEED # 제자리 회전 탐색

            # 주행 중 실시간 장애물 체크
            self.avoid_obstacles()
            time.sleep(0.1)  # 루프 주기 제어 (CPU 부하 감소)

    def stop_robot(self):
        self.motor.speed = 0, 0

    def complete_service(self):
        self.stop_robot()
        self.speaker.tune = 100, 100  # 완료 알림음
        time.sleep(1)
        self.speaker.tune = 0, 0

if __name__ == "__main__":
    robot = SunFollower()
    
    if robot.check_weather_condition():
        robot.drive_system(timeout_sec=120)