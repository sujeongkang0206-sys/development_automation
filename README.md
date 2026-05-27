# User Management FastAPI Docker Deployment

이 프로젝트는 FastAPI 기반 사용자 관리 API를 Docker와 Docker Compose로 실행할 수 있도록 구성되어 있습니다.

## 파일 설명
- `Dockerfile`: Python 이미지를 사용해 FastAPI 애플리케이션을 빌드합니다.
- `docker-compose.yml`: 웹 애플리케이션과 MySQL 데이터베이스를 함께 실행합니다.
- `requirements.txt`: FastAPI와 Uvicorn 실행에 필요한 Python 패키지 목록입니다.
- `.env.example`: 환경 변수 템플릿입니다.

## 실행 방법

1. `.env.example` 파일을 복사하고 필요한 값을 설정합니다.
   ```bash
   copy .env.example .env
   ```
2. Docker Compose로 서비스 시작.
   ```bash
   docker compose up --build
   ```
3. 브라우저에서 확인.
   ```text
   http://localhost:8000/docs
   ```

## 개발/배포 고려 사항
- 현재 서비스는 `backend/app/main.py`에 있는 FastAPI 애플리케이션을 실행합니다.
- `docker-compose.yml`은 `db` 서비스로 MySQL을 제공합니다.
- 실제 배포 시에는 `DATABASE_URL`을 배포 환경에 맞게 구성하고, 불필요한 개발 모드를 제거하세요.
