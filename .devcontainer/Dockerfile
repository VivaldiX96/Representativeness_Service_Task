# Using the official image as a parent image
FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

# Setting the working directory in the container
WORKDIR /app

# Copying the requirements file into the container at /app
COPY requirements.txt .

# Exposing the port on which the application will listen
EXPOSE 8090

# Installing the required libraries
RUN pip install --no-cache-dir -r requirements.txt

# Adding the application files to the image
COPY . .

# Running the application using CMD
CMD [ "python", "./app.py" ]