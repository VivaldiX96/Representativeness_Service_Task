import asyncio
from flask import Flask, jsonify
from fastapi import FastAPI
from services import train_models
from schemas import NumbersInput

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
@app.post("/input_array/")
async def validate_numbers(numbers_input: NumbersInput):
    return{"message":"Correct input received. Proceeding."}

async def dummy_function():
    print("Dummy function started")
    await asyncio.sleep(20)
    print("Dummy function finished")

async def check_function_status():
    if 'task_coro' in globals() and not task_coro.done():
        return "Function is running"
    else:
        return "Function is not running"

@app.get("/task_status")
async def get_task_status():
    return await check_function_status()

@app.get("/start_task")
async def start_task():
    global task_coro
    task_coro = asyncio.create_task(dummy_function())
    return "Task started"

async def dummy_machine_learning_task():
    print("Machine learning process started")
    await asyncio.sleep(20)  # Dummy 20-second waiting task
    success = True  # Simulate success or failure of the process, you can replace this with actual logic
    if success:
        return "Regression model"  # Return the learned regression model
    else:
        return None  # Return None to indicate failure

async def check_task_status():
    if 'task_coro' in globals() and not task_coro.done():
        return "Task is running"
    elif 'task_coro' in globals() and task_coro.done():
        result = await task_coro
        if result:
            return "Task finished successfully"
        else:
            return "Task finished but failed"
    else:
        return "No task running"

@app.get("/task_status")
async def get_task_status():
    return await check_task_status()

@app.get("/start_task")
async def start_task():
    global task_coro
    task_coro = asyncio.create_task(dummy_machine_learning_task())
    return "Task started"
 