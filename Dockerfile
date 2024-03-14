FROM alpine:3.14

WORKDIR /usr/src/app

COPY . .

RUN apk add --no-cache python3 py3-pip curl && \
    python3 -m venv /venv && \
    . /venv/bin/activate && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    adduser -D myuser

EXPOSE 80

USER myuser

ENTRYPOINT ["/bin/sh", "-c", ". /venv/bin/activate && exec python /usr/src/app/main.py \"$@\"", "--"]

HEALTHCHECK --interval=5m --timeout=3s \
  CMD curl -f http://localhost/ || exit 1