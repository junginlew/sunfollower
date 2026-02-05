# SUNFOLLOWER: 자율 주행 일조 로봇 제어 시스템
반려식물의 충분한 일조량 확보를 위해 조도 센서 기반의 광원 추적 및 실시간 장애물 회피 기능을 갖춘 자율 주행 로봇 제어 시스템.

# 1. 핵심 기능

실시간 광원 추적 (Light Tracking): 주변 환경을 360° 탐색하여 가장 밝은 지점을 식별하고, 목표 조도에 도달할 때까지 최적의 경로로 주행합니다.

복합 장애물 회피 (Obstacle Avoidance): 주행 중 물리적 충돌 감지 시 '후진-회전-우회'로 이어지는 시나리오 기반의 회피 기동을 수행하여 고립 상황을 방지합니다.

상황 인지 주행 (Context-aware Driving): OpenWeather API를 연동하여 현재 지역의 날씨를 확인합니다. 강우 등 야외 주행이나 일조에 부적합한 기상 조건 발생 시 시스템을 자동으로 정지시키는 Failsafe 기능을 갖추고 있습니다.

# 2. 기술 스택
Language: Python 3.x

Hardware: MODI Robotics Kit (Motor, Environment, Speaker, Button modules) 

API: OpenWeatherMap API 

Environment Management: python-dotenv (Security)
