# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install gcc & cron
RUN apt-get update && apt-get install gcc -y && apt-get clean

# Install the requirements
COPY requirements.txt /
RUN pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt

# Set the working directory and install the demo package
WORKDIR /pipeline
RUN mkdir -p -m777 /input
COPY ./py .

# Log stuff

RUN mkdir -p -m777 /mnt/log

# Run api?
#CMD tail -f /dev/null
ENTRYPOINT ["python", "/pipeline/main.py"]