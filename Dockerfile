# Use the official Python image as the base image
# synology nas platform
FROM --platform=linux/amd64 python:3.8-slim-buster as build 

# macOS platform
# FROM --platform=linux/arm64 python:3.8-slim-buster  

# Set the working directory
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt requirements.txt

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Set the command to run your application
CMD [ "python3", "app.py"]