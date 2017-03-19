FROM python:2.7.12

ADD requirements /code/requirements

RUN pip install -r /code/requirements/testing.txt

ADD . /code