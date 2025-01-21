# Python 이미지를 기반으로 생성
FROM python:3.9

# 작업 디렉토리 설정
WORKDIR /app

# requirements.txt 파일을 컨테이너로 복사
COPY requirements.txt /app/

# 필요한 Python 라이브러리 설치
RUN pip install --no-cache-dir -r requirements.txt

# 프로젝트 파일 복사
COPY . /app/

# Django에서 사용하는 포트 열기
EXPOSE 8000

# Django 서버 실행
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
