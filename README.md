This program generates a REST service that allows:

- to train the ML model on a set of objects (an object being a set of a constant size containing numbers),
- to check the status of the training (still in progress, finished or failed)
- to use the model trained on the lately delivered objects to provide predictions of new values

Pylance version must be 2023.12.1 or lower (that's why it's specified in the VSCode extensions section in devcontainer.json) - otherwise errors will occur when trying to initialize an int type variable within a certain values interval

**Instruction on how to run the program from a Docker:**

    - in order to build the image, open the command prompt, change directory to where the Dockerfile is stored and run "docker build -t repr-service .".

    - to run the image in Docker, run "docker run -d --name repr-service-container -p 80:80 repr-service" in the command line. The server should start automatically from a command in the Dockerfile.

    - to see the endpoints, open the browser on the address "localhost:80/docs". Make sure that port 80 is unoccupied before that, otherwise contact with the app may be obstructed.

_Optional - Instruction on how to run the devcontainer in VSCode:_

    - In order to run this program in a devcontainer with the required dependencies installed, you need to have Docker running on your machine (you can choose a version for your machine and download it from https://docs.docker.com/desktop/). It cooperates with VSCode (https://code.visualstudio.com/Download) by providing a container inside which you will run the program.
    - Install the Dev Containers extension if it is not installed yet in VSCode on your machine (identifier: ms-vscode-remote.remote-containers).
    - Open VSCode in the directory where this repo is located
    - Press Ctrl + Shift + P to show and run commands in the search field on top of the VSCode window
    - Choose the option "Dev Containers: Reopen in Container". You can find it if you start typing ">reopen..." in the search field. Make sure that Docker is running by the time you choose this option.
    - To run the server, first cd to ./devcontainer/app - then type "uvicorn main:app --host 0.0.0.0 --port 80 --reload" in the command line in the IDE when you are in the working directory in the program's container - the uvicorn service will not be launched automatically if you open the devcontainer, the command line has to be handled by the user

On the first run of the program, please generate a batch of training data for the ML models executing the function in GET /training_data endpoint and supply that data to the train_models endpoint in order to train the first batch of models and be able to grab them to predict results for new independent variables.
In parameters.py, there is a global constant ARRAYS_AMOUNT that makes it possible to generate more or less training data to be delivered to the regression model for it's training
