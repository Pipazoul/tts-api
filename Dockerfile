

FROM python:3.9-slim-buster

RUN apt update
RUN apt install espeak -y

WORKDIR /app
COPY . ./
RUN ls
RUN pip install -r requirements.txt

ENTRYPOINT [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" ]