FROM python:3.8-buster

COPY src src
COPY app.py .
COPY config.yml .
COPY __init__.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 8080

ENTRYPOINT python app.py
