## SUNFOLLOWER: 자율 주행 일조 로봇 제어 시스템
반려식물의 충분한 일조량 확보를 위해 조도 센서 기반의 광원 추적 및 실시간 장애물 회피 기능을 갖춘 자율 주행 로봇 제어 시스템.

## 핵심 기능

실시간 광원 추적: 360° 회전을 하며 주변 조도 값을 스캔하고, 임계치 이상의 광원을 발견하면 해당 방향으로 직진함.

장애물 회피: 주행 중 물리적 충돌 감지 시 '후진-회전-우회'로 이어지는 회피 기동을 수행함.

상황 인지 주행: OpenWeatherMap API를 연동하여 현재 지역의 날씨를 확인함. 강우 등 일조에 부적합한 기상 조건 발생 시 시스템을 자동으로 정지시킴.

## 기술 스택
Language: Python

Hardware: MODI Robotics Kit (Motor, Environment, Speaker, Button modules) 

API: OpenWeatherMap API 

Environment Management: python-dotenv (Security)
