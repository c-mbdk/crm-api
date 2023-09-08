FROM python:3.10.9-alpine

RUN apk update
RUN pip install --no-cache-dir pipenv

WORKDIR /usr/src/app
COPY Pipfile Pipfile.lock bootstrap.sh ./
COPY tests app.py README.md ./

RUN pipenv install --system --deploy

EXPOSE 5000
ENTRYPOINT ["/usr/src/app/bootstrap.sh"]