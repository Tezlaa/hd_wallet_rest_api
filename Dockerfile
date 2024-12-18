FROM python:3.12-slim

WORKDIR /hd_wallet_rest_api

ENV PYTHONPATH="${PYTHONPATH}:/hd_wallet_rest_api"

RUN apt update && apt install -y build-essential python3-dev libssl-dev gcc
ADD requirements.txt /hd_wallet_rest_api/
RUN pip install -r requirements.txt --no-cache-dir

COPY . .

EXPOSE 5000