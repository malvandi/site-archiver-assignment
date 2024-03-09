# Use an appropriate base image
FROM python:3.13-rc-bullseye

# Set the working directory inside the container
WORKDIR /app

# Define a volume for /app inside the container
VOLUME /app

# Define the entry point for the container
ENTRYPOINT ["python", "fetch.py"]