# Use an appropriate base image
FROM python:3.12.2-bullseye

# Set the working directory inside the container
WORKDIR /app

# Define a volume for /app inside the container
VOLUME /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Define the entry point for the container
ENTRYPOINT ["python", "archive.py"]