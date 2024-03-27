import asyncio
from fastapi import FastAPI
from services import train_models, generate_data, dump_models, predict_from_models_array, check_training_status
from schemas import NumbersInput
from models import MachineLearningData, IndVariablesInput
from typing import List
from parameters import NUMBER_OF_MODELS


from time import sleep   ### for testing on dummy tasks

app = FastAPI()


@app.get("/training_data")
async def generate_training_data():
    return await generate_data()



# endpoint for initiation of the model training on the data delivered 
# by the User - preferably, copied after generating from the training_data endpoint
@app.post("/train-models")
async def train_models_on_supplied_data(datasets_batch: list[MachineLearningData]):    
    trained_models = await train_models(datasets_batch)
    dump_models(trained_models)
    return {"message": f"{NUMBER_OF_MODELS} models trained and saved in the /trained_models folder"}

### Please generate a batch of training data for the ML models and supply the to the train_models endpoint in order to
### train the first batch of models and be able to grab them to predict for new independent variables    


@app.get("/task_status")
async def get_task_status():
    return await check_training_status()


@app.post("/predict")
async def predict_on_new_data(user_data_array: list[IndVariablesInput]):
    return await predict_from_models_array(user_data_array)







