FROM python:3.14.2-bookworm

COPY . .

RUN pip install -r requirements.txt