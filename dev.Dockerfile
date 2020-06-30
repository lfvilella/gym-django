FROM python:3.7

EXPOSE 8000

ADD . /deploy

WORKDIR /deploy

RUN pip install --upgrade pip && pip install -r requirements-dev.txt

CMD python manage.py runserver 0.0.0.0:8000
