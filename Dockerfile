###############
# BUILD IMAGE #
###############
FROM python:3.10-slim-buster
#FROM python:3.10-alpine

# Setting working dir
WORKDIR /usr/local/src/Rubus

# Install dependt libs
COPY requirements.txt  ./

# Reinstall dependt libs
RUN pip install --no-cache-dir -r requirements.txt

# Install dependt libs
#RUN pip install -r requirements.txt

# Copy all the file to workdir
COPY .  .