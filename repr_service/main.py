from flask import Flask, jsonify
from fastapi import FastAPI
from services import train_model

from time import sleep   ### for testing on dummy tasks

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "hello world"}








# endpoint for initiation of the model training

#app. ...
#async def ...



# endpoint for checking the training status
#app.get
#

"""
app = Flask(__name__)

@app.route("/api/training-status")
def get_training_status_route():
  status = get_training_status()
  return jsonify(status)

if __name__ == "__main__":
  app.run()

  """