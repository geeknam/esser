FROM python:2.7.12

ADD requirements.txt /code/requirements.txt

RUN pip install -r /code/requirements.txt