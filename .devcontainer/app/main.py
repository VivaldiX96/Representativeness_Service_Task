import asyncio
import os
from pathlib import Path
import random
from fastapi import FastAPI
from sklearn import base
from services import generate_data, dump_models, predict_from_models_array, check_training_status
from models import MachineLearningData, IndVariablesInput
from typing import List
from parameters import NUMBER_OF_MODELS, N_ESTIMATORS
from multiprocessing import Pool
from datetime import datetime

from sklearn.ensemble import RandomForestRegressor

from multiprocessing import Pool

from time import sleep

app = FastAPI()


TRAINED_MODELS_PATH_NAME = 'trained_models' # name of a folder created (once) for all the trained models

STATUS_FILE_NAME = "latest_training_status"

current_dir = Path.cwd()
status_file_name = STATUS_FILE_NAME
status_file_path = os.path.join(current_dir, status_file_name)

num_cores = os.cpu_count() # current number of CPU cores, 
                        # to be used as number of threads in C++

def train_one_model(dataset):

    one_model_training_start = datetime.now().strftime("%Y%m%d-%H:%M:%S")

    X = [data_pair.ind_vars for data_pair in dataset] #list of lists of independent variables
    y = [data_pair.dep_var for data_pair in dataset] #list of dependent variables
         


        
    print(f"training a model - started at {datetime.now().strftime("%Y.%m.%d-%H:%M:%S")}...")
    regressor = RandomForestRegressor(n_estimators = N_ESTIMATORS, random_state = random.randint(0, 42)) # 42 is a lucky number in ML
    try:
        regressor.fit(X, y) # training a model
        sleep(4)
            
    except Exception as e:
        print(f"model training failed - exception occurred: {e}")
        training_failure_time = datetime.now().strftime("%Y%m%d-%H:%M:%S")
        status_message = f"Training of one or more models failed with the exception {e}. Training started at {one_model_training_start}, ended at {training_failure_time}."
        with open(status_file_path, 'w') as status_file:
            status_file.write(status_message)
        return None
    return regressor

def train_models(raw_datasets_batch: List[MachineLearningData]):
    
    training_start_time = datetime.now().strftime("%Y%m%d-%H:%M:%S")
    status_message = f"A new training of {NUMBER_OF_MODELS} models was started at {training_start_time}"
        
    


    with open(status_file_path, 'w') as status_file:
        status_file.write(status_message)

    trained_models = []
    

    datasets = []

    pool = Pool(processes=num_cores) # number of processes of machine learning we want to start concurrently - in this case it is the number of models
                                     # the data for models will be split into as many datasets as there are models
    

    ###############

    for raw_dataset in raw_datasets_batch:
        # Getting machine learning data from each ml_data field in JSON input
        dataset = raw_dataset.ml_data
        datasets.append(dataset)


        
        #trained_models.append(regressor) #adding a freshly trained model to the batch of models to be saved in the trained_models folder
    
    ###############

    

    trained_models = pool.map(train_one_model, datasets)
    
    pool.close()
    pool.join()

    training_end_time = datetime.now().strftime("%Y%m%d-%H:%M:%S")

    #checking if the list we get at the end is full of BaseEstimators - if just one position is not of a type of BaseEstimator, no success message is printed
    if len(trained_models) == NUMBER_OF_MODELS and all(isinstance(elem, base.BaseEstimator) for elem in trained_models): 
        status_message = f"Training started at {training_start_time} finished successfully. Training ended at {training_end_time}." 
        with open(status_file_path, 'w') as status_file:
            status_file.write(status_message)
        print(status_message)
        return trained_models
    else:
        return 





@app.get("/training_data")
async def generate_training_data():
    return await generate_data()

### Multiprocess version:
# endpoint for initiation of the model training on the data delivered 
# by the User - preferably, copied after generating from the training_data endpoint
@app.post("/train-models")
async def train_models_on_supplied_data(datasets_batch: list[MachineLearningData]):    
    #### multiprocessing version >>>
    #async with ProcessPoolExecutor() as executor:
    #    trained_models = await executor.map(train_models, datasets_batch)
    #### <<< multiprocessing version
    ###
    ### CHANGED LINE: # trained_models = await train_models(datasets_batch)
    trained_models = train_models(datasets_batch)
    ###
    dump_models(trained_models)
    return {"message": f"{NUMBER_OF_MODELS} models trained and saved in the /trained_models folder"}




# endpoint for initiation of the model training on the data delivered 
# by the User - preferably, copied after generating from the training_data endpoint
# @app.post("/train-models")
# async def train_models_on_supplied_data(datasets_batch: list[MachineLearningData]):    
#     trained_models = await train_models(datasets_batch)
#     dump_models(trained_models)
#     return {"message": f"{NUMBER_OF_MODELS} models trained and saved in the /trained_models folder"}

### Please generate a batch of training data for the ML models and supply the to the train_models endpoint in order to
### train the first batch of models and be able to grab them to predict for new independent variables    


@app.get("/task_status")
async def get_task_status():
    return await check_training_status()


@app.post("/predict")
async def predict_on_new_data(user_data_array: list[IndVariablesInput]):
    return await predict_from_models_array(user_data_array)

