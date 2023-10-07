FROM python:3.11-alpine3.18

WORKDIR /backend

COPY requirements.txt /backend/

RUN pip install -r requirements.txt

COPY . /backend/

CMD python manage.py run

