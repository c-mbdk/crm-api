FROM python:3.9.5-slim-buster

RUN apt-get update \
    && pip install psycopg2
RUN pip install --no-cache-dir pipenv

WORKDIR /usr/src/app
COPY Pipfile Pipfile.lock bootstrap.sh ./
COPY tests app.py README.md ./

RUN cd /usr/src/app && pipenv install --system

EXPOSE 5000
ENTRYPOINT ["/usr/src/app/bootstrap.sh"]
