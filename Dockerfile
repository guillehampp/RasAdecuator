FROM alpine:3.14.0

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Run commands in your new Alpine container
# trunk-ignore(terrascan/AC_DOCKER_0010)
RUN apk add --no-cache python3=3.9.7-r3 py3-pip=21.2.4-r0 curl && \
    pip install --no-cache-dir -r requirements.txt && \
    python3 -m venv /venv && \
    . /venv/bin/activate && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    adduser -D myuser

# Make port 80 available to the world outside this container
EXPOSE 80

# Change to non-root user
USER myuser

# Run main.py when the container launches, and pass arguments to it
ENTRYPOINT ["/bin/sh", "-c", ". /venv/bin/activate && exec python /usr/src/app/main.py \"$@\"", "--"]

# Add healthcheck
HEALTHCHECK --interval=5m --timeout=3s \
  CMD curl -f http://localhost/ || exit 1