FROM python:3.13-alpine

RUN mkdir -p app

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src/*.py .

EXPOSE 8080

CMD ["python3", "server.py"]