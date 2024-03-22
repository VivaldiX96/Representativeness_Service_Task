This program generates a REST service that allows:

- to train the ML model on a set of objects (an object being a set of a constant size containing numbers),
- to check the status of the training (still in progress, finished or failed)
- to use the model trained on the lately delivered objects to provide predictions of new values

Pylance version must be 2023.12.1 or lower (that's why it's specified in the VSCode extensions section in devcontainer.json) - otherwise errors will occur when trying to initialize an int type variable within a certain values interval

**Instruction on how to run the program from a Docker:**

- to make sure you are in /workspaces/Representativeness_Service_Task/repr_service - run "cd repr_service" in the command line inside the container

- run the server with the command "uvicorn main:app --reload"

- to see the endpoints, open the browser on the address "localhost:8000/docs". Make sure that port 8000 is unoccupied before that, otherwise contact with the app may be obstructed.

_Optional - Instruction on how to run the devcontainer in VSCode:_

- In order to run this program in a devcontainer with the required dependencies installed, you need to have Docker running on your machine (you can choose a version for your machine and download it from https://docs.docker.com/desktop/). It cooperates with VSCode (https://code.visualstudio.com/Download) by providing a container inside which you will run the program.
- Install the Dev Containers extension if it is not installed yet in VSCode on your machine (identifier: ms-vscode-remote.remote-containers).
- Open VSCode in the directory where this repo is located
- Press Ctrl + Shift + P to show and run commands in the search field on top of the VSCode window
- Choose the option "Dev Containers: Reopen in Container". You can find it if you start typing ">reopen..." in the search field. Make sure that Docker is running by the time you choose this option.
- To run the server, type "uvicorn main:app --reload" in the command line in the IDE when you are in the working directory in the program's container - make sure that the command prompt looks like this: "vscode ➜ /workspaces/Representativeness_Service_Task"
