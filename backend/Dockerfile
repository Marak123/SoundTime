FROM python:3.11-alpine3.18

ENV PYTHONUNBUFFERED 1

WORKDIR /django

COPY ./requirements.txt ./requirements.txt


RUN apk update && \
    python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps build-base postgresql-dev musl-dev linux-headers gcc python3-dev && \
    /py/bin/pip install -r ./requirements.txt && \
    apk del .tmp-deps

RUN apk add --update --no-cache ffmpeg

RUN adduser --disabled-password --no-create-home django && \
    mkdir -p /var/www/web/static && \
    mkdir -p /var/www/web/media/thumbnail && \
    mkdir -p /var/www/web/media/audio && \
    chown -R django:django /var/www/web && \
    chmod -R 755 /var/www/web


ENV PATH="/scripts:/py/bin:$PATH"

COPY . .

RUN python manage.py collectstatic --noinput



COPY ./scripts /scripts

RUN chmod +x /scripts/run.sh



USER django

CMD ["run.sh"]