FROM python:3.9-alpine3.13
LABEL maintainer="danlopatenco@gmail.com"

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY ./requirements/requirements.txt /tmp/requirements.txt
COPY ./requirements/requirements.dev.txt /tmp/requirements.dev.txt


COPY . /app


WORKDIR /app
EXPOSE 8585

ARG DEV=true
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \ 
    apk add --update --no-cache --virtual .tmp-build-deps \ 
        build-base postgresql-dev musl-dev libffi-dev python3-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
    then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \ 
    rm -rf /tmp && \
    apk del .tmp-build-deps



ENV PATH="/py/bin:$PATH"

ENTRYPOINT [ "/app/entrypoint.sh" ]