FROM python:latest

RUN apt-get update && apt-get install -y iputils-ping
RUN pip install click

COPY . .

ENTRYPOINT [ "python3", "script.py"]