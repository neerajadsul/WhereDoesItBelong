FROM python:3.12.3-slim-bullseye 

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 8000

ENTRYPOINT [ "python3" ]
