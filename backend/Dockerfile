FROM python:3.9-alpine3.13
LABEL maintainer="francesco.bursi@htomail.it"

ENV PYTHONUNBUFFERRED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app

WORKDIR /app

#tell to the container to expose port XXXX to our machine
EXPOSE 8000

ARG DEV=false
#u do venv to avoid conflict dep inside the container that can happen
#with django dependencies
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache procps &&\
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ;\
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

ENV PATH="/py/bin:$PATH"

COPY ./script/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//g' /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./script/start.sh /start.sh
RUN sed -i 's/\r$//g' /start.sh
RUN chmod +x /start.sh

COPY ./script/worker_start.sh /worker_start.sh
RUN sed -i 's/\r$//g' /worker_start.sh
RUN chmod +x /worker_start.sh

COPY ./script/beat_start.sh /beat_start.sh
RUN sed -i 's/\r$//g' /beat_start.sh
RUN chmod +x /beat_start.sh

USER django-user

ENTRYPOINT ["/entrypoint.sh"]