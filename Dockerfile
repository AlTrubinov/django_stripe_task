FROM python:3.10.6

ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /usr/src/django_stripe_task

RUN pip install --upgrade pip

COPY ./requirements.txt /usr/src/requirements.txt
RUN pip install --no-cache-dir -r /usr/src/requirements.txt

COPY . /usr/src/django_stripe_task