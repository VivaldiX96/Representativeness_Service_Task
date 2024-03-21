This program generates a REST service that allows:

- to train the ML model on a set of objects (an object being a set of a constant size containing numbers),
- to check the status of the training (still in progress, finished or failed)
- to use the model trained on the lately delivered objects to provide predictions of new values

Pylance version must be 2023.12.1 or lower (that's why it's specified in the VSCode extensions section in devcontainer.json) - otherwise errors will occur when trying to initialize an int type variable within a certain values interval

### add instruction on how to run the devcontainer in VSCode

To run the server, type "uvicorn main:app --reload" in the command line in the IDE when you are in the working directory in the program's container: vscode ➜ /workspaces/Representativeness_Service_Task
