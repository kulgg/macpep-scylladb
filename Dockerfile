FROM python:3.11
RUN python -m pip install poetry
RUN apt update
RUN apt install net-tools
RUN apt install telnet