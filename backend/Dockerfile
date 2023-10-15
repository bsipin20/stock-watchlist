FROM python:3.11-alpine3.18

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app/
COPY .env .env

CMD python manage.py run

