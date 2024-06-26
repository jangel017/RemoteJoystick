FROM ubuntu:jammy

# Update package list and install necessary packages
RUN apt-get update && \
    apt-get install -y python3 python3-pip

# Install Python packages
RUN pip3 install Flask flask_socketio flask_cors python-uinput

RUN apt install sudo
