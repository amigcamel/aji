FROM python:3.6.5-alpine3.7
ARG SECRET_KEY
ARG EMAIL_HOST_USER
ARG EMAIL_HOST_PASSWORD
ENV SECRET_KEY=$SECRET_KEY
ENV EMAIL_HOST_USER=$EMAIL_HOST_USER
ENV EMAIL_HOST_PASSWORD=$EMAIL_HOST_PASSWORD
WORKDIR /app
COPY . $WORKDIR

# test variables
RUN test -n "$SECRET_KEY"

# build
RUN apk update && \
    apk add build-base python3-dev linux-headers pcre-dev jpeg-dev zlib-dev postgresql-dev && \
    pip install -r requirements.txt

CMD ./entrypoint.sh
