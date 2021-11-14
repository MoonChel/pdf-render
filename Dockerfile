FROM python:3.9

RUN mkdir /app
WORKDIR /app

ENV PYTHONUNBUFFERED = 1

COPY *requirements.in /app/

RUN pip install --no-cache-dir -r requirements.in -r tasks_requirements.in

COPY . /app

EXPOSE 8000
EXPOSE 5555