# Use the official Python 3.10 image from the Docker Hub
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY ../litemultiagent/requirements.txt .

# Copy the env.example file into the container at /app
COPY ../env.example .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create a .env file from env.example
RUN cp env.example .env

# Copy the rest of the application code into the container at /app
COPY .. .

# Command to run the application
