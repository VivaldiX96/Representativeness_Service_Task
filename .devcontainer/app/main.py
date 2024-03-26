import asyncio
from flask import Flask, jsonify
from fastapi import FastAPI
from services import dummy_function, train_models, generate_data, dump_models
from schemas import NumbersInput
from models import MachineLearningData
from typing import List


from time import sleep   ### for testing on dummy tasks

app = FastAPI()

global TASK_CORO # declaring a variable for monitoring of current training status

@app.get("/")
async def root():
    return {"message": "hello world"}



@app.get("/training_data")
async def generate_training_data():
    return await generate_data()


"""
app = Flask(__name__)

@app.route("/api/training-status")
def get_training_status_route():
  status = get_training_status()
  return jsonify(status)

if __name__ == "__main__":
  app.run()

  """
@app.post("/input_array")
async def validate_numbers(numbers_input: NumbersInput):
    return{"message":"Correct input received. Proceeding."}

# async def dummy_function():
#     print("Dummy function started")
#     await asyncio.sleep(20)
#     print("Dummy function finished")


# endpoint for initiation of the model training on the data delivered 
# by the User - preferably, copied after generating from the training_data endpoint
@app.post("/train-models")
async def train_models_on_JSON(datasets_batch: list[MachineLearningData]):
    
    trained_models = await train_models(datasets_batch)
    dump_models(trained_models)
    #return {"trained_models": trained_models, "training_success": training_success} ###### CHANGE - only dump the models, not try to return them




@app.get("/start_task")
async def start_task():
     #
    TASK_CORO = asyncio.create_task(dummy_function())
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
    if 'TASK_CORO' in globals() and not TASK_CORO.done():
        return "Training in progress..."
    elif 'TASK_CORO' in globals() and TASK_CORO.done():
        result = await TASK_CORO
        if result:
            return "Model training finished successfully"
        else:
            return "Model training finished but failed"
    else:
        return "No model is being currently trained"

@app.get("/task_status")
async def get_task_status():
    return await check_task_status()

@app.get("/start_task")
async def start_task():
    global TASK_CORO
    TASK_CORO = asyncio.create_task(dummy_machine_learning_task())
    return "Task started"
 
# @app.delete("/task-disruptor")
# async def end_task_with_a_failure(): 
