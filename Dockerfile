FROM python:3.6.5-alpine3.7
WORKDIR /web
COPY . $WORKDIR
run apk update && apk add build-base python3-dev linux-headers pcre-dev jpeg-dev zlib-dev postgresql-dev
RUN pip install -r requirements.txt && \
    python manage.py collectstatic --noinput
CMD ["uwsgi", "--uid", "root", "--master", "--http", "0.0.0.0:8000", "--module", "aji.wsgi", "--static-map", "/static_all=static_all"]
