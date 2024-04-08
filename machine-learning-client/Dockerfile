FROM python:3

WORKDIR /

RUN pip install pipenv

COPY Pipfile Pipfile.lock /

RUN pipenv install --system