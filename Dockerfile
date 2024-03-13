# Use an official Alpine image as a parent image
FROM alpine:latest

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Run commands in your new Alpine container
RUN apk add --no-cache python3 py3-pip && \
    python3 -m venv /venv && \
    . /venv/bin/activate && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run main.py when the container launches, and pass arguments to it
ENTRYPOINT ["/bin/sh", "-c", ". /venv/bin/activate && exec python /usr/src/app/main.py \"$@\"", "--"]