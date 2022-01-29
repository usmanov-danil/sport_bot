FROM python:3.9-slim-buster

WORKDIR /app

USER root
ENV PYTHONUNBUFFERED 1

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ARG ENV
ARG CONFIG

RUN pip3 install pipenv

COPY ./telegram/Pipfile .
COPY ./telegram/Pipfile.lock .
RUN if [ "$ENV" = "dev" ]; then \
    pipenv install --dev --deploy --clear --system --ignore-pipfile; \
else \
    pipenv install --deploy --clear --system --ignore-pipfile; \
fi

COPY ./telegram .
COPY ./configs/$CONFIG ./config.json

ENV ENV=$ENV
ENTRYPOINT ["python", "/app/runpoint.py"]
