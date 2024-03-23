# Using the official image as a parent image
FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

# Setting the working directory in the container
WORKDIR /code

# Copying the requirements file into the container at /app
COPY ./requirements.txt /code/requirements.txt

# Installing the required libraries
RUN pip install --no-cache-dir -r /code/requirements.txt

#RUN MKDIR /code/app

# Adding the application files to the image
COPY ./app /code/app

# Setting the working directory to /app
WORKDIR /code/app


# Running the server using CMD
# in order to run the server in a VSCode Devcontainer, 
# first cd manually to /app using command prompt in VSCode:
# cd .devcontainer/app
# and then run the command to start the server: uvicorn main:app --host 0.0.0.0 --port 80 --reload
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]