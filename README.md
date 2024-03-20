This program generates a REST service that allows:

- to train the ML model on a set of objects (an object being a set of a constant size containing numbers), and then...
- to use the model trained on the lately delivered objects to provide predictions of new values

Pylance version must be 2023.12.1 or lower (that's why it's specified in the VSCode extensions section in devcontainer.json) - otherwise errors will occur when trying to initialize an int type variable within a certain values interval
