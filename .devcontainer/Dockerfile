# Using the official image as a parent image
FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

# Setting the working directory in the container
WORKDIR /code

# Copying the requirements file into the container at /app
COPY ./requirements.txt /code/requirements.txt

# Installing the required libraries
RUN pip install --no-cache-dir -r /code/requirements.txt

# Adding the application files to the image
COPY ./app /code/app

# Running the server using CMD
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]