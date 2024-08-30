FROM python:3.9.5-slim AS builder

RUN pip install --no-cache-dir pipenv

WORKDIR /usr/src/app
COPY Pipfile Pipfile.lock bootstrap.sh ./
COPY tests run.py README.md src config.py .env ./

RUN cd /usr/src/app && pipenv install --system

EXPOSE 5000
ENTRYPOINT ["/usr/src/app/bootstrap.sh"]
