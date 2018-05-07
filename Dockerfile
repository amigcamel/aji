FROM python:3.6.5-alpine3.7
ARG SECRET_KEY
ARG EMAIL_HOST_USER
ARG EMAIL_HOST_PASSWORD
WORKDIR /app
COPY . $WORKDIR

# test variables
RUN test -n "$SECRET_KEY"
RUN test -n "$EMAIL_HOST_USER"
RUN test -n "$EMAIL_HOST_PASSWORD"

# build
RUN apk update && apk add build-base python3-dev linux-headers pcre-dev jpeg-dev zlib-dev postgresql-dev
RUN pip install -r requirements.txt && \
    python manage.py collectstatic --noinput
