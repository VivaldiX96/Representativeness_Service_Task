from datetime import datetime
from pathlib import Path
import random
from time import sleep
from typing import List

from joblib import dump
from models import VariablesRow, MachineLearningData
from sklearn import base
from sklearn.ensemble import RandomForestRegressor
from parameters import NUMBER_OF_MODELS, INDVARS_ARRAY_SIZE, ARRAYS_AMOUNT, K_NEAREST_NEIGHBOURS
import asyncio
import math

TRAINED_MODELS_PATH_NAME = 'trained_models' # name of a folder created (once) for all the trained models

async def train_models(datasets_batch: List[MachineLearningData]):
    trained_models = []
    training_success = None

    for dataset in datasets_batch:
        # Importing the dataset
        # getting the array of all independent variables into the X variable
        X = [pair[0] for pair in dataset]
        
        # getting the array of all dependent variables into the y variable
        y = [pair[1] for pair in dataset]    

        await asyncio.sleep(5)
        regressor = RandomForestRegressor(n_estimators = 10, random_state = random.randint(0, 42))
        try:
            regressor.fit(X, y) # training a model
            
        except:
            print("model training failed")
            training_success = False
        
        trained_models.append(regressor)
    
    if len(trained_models) == NUMBER_OF_MODELS:
        training_success = True
        print("training successful")
        return trained_models
    else:
        training_success = False
        print("training of one or more models failed")
        return training_success
    





    # Function generating a set of arrays of the chosen size 'size' with arrays_amount elements;
# It returns a list of arrays of random numbers to be used as independent variables in ML training
def generate_arrays(array_size: int, 
                          #number of arrays must be above a number that provides 
                          #enough examples to train the model but is not excessively high
                          arrays_amount: int):

    
    # Initialize an empty list to store the generated arrays
    arrays = []
    
    # Loop over the specified number of arrays to generate
    for i in range(arrays_amount):
        # Generate an array of size 'size' comprising of numbers from 0 to 100
        array = [random.uniform(0, 100) for _ in range(array_size)]
        
        # Add the generated array to the list of arrays
        arrays.append(array)
    
    return arrays


#generated_arrays = generate_arrays(INDVARS_ARRAY_SIZE, ARRAYS_AMOUNT) # all arrays of independent variables are generated


# Function takes the training_arrays list of training arrays generated by generate_arrays,
# and splits it randomly into NUMBER_OF_MODELS, keeping the order of the numbers in individual lists
def split_data_for_models(training_arrays, PartsNumber: int): #maybe change PartsNumber to local variable?
    
    # Create and shuffle indices
    indices = list(range(len(training_arrays)))
    random.shuffle(indices)

    # Split data using shuffled indices
    split_data = [[] for _ in range(PartsNumber)]
    for i, idx in enumerate(indices):
        split_data[i % PartsNumber].append(training_arrays[idx])
  
    split_data = [training_arrays[i::PartsNumber] for i in range(PartsNumber)]
    
    return split_data

###split_training_arrays = split_data_for_models(generated_arrays, NUMBER_OF_MODELS)
###print(split_training_arrays)

# Function calculating representativeness values for all the objects in a given list
# and filling a dict of the calculated repr. values for each object
def repr_calc_in_a_set(objects: list):
    #For each object, calculating distances from all other objects
    sublist_size = len(objects)
    mldata_items = []# dictionary of pairs object : representativeness, with the size of the sublist taken by the function
    for position in range(sublist_size):
        # calculating the euclidean distance - squared difference of every pair of numbers
        obj = objects[position]
        distances_sum = 0
        neighbours = [element for element in objects if element != objects[position]]
        neighbours_with_distances = []
        #Calculating the distances to all neighbours to find the K nearest neighbours
        for neighbour in neighbours:
            distance = math.sqrt(sum((a - b)**2 for a, b in zip(obj, neighbour)))
            # adding up all the distances from the current considered object ot the rest of the neighbors
            neighbours_with_distances.append([neighbour, distance])
            
            # print(f"distance = {distance}")  # printing for visual checking of example results
        
        nearest_neighbours = sorted(neighbours_with_distances, key=lambda x: x[1], reverse=True)[:K_NEAREST_NEIGHBOURS]
        # adding up all K nearest neighbours' distances for the object, taking the average and calculating representativeness based on it
        distances_sum = sum(obj_and_dist[1] for obj_and_dist in nearest_neighbours) 
        avg_distance = distances_sum / K_NEAREST_NEIGHBOURS
        depvar = 1 / (1 + avg_distance) #dependent variable being the calculated representativeness
         
        # appending the representativeness value to a list of objects mapped to their repr. values
        mldata_items.append(VariablesRow(indvars=obj, depvar=depvar)) #appending mutable elements in order to enable feature scaling later
    #print(f"list of representativeness:")
    #print(mldata_items) #just for value checking/program observation
    return MachineLearningData(mldata=mldata_items)

async def generate_data():
    objects_to_reprs_batch = []
    split_training_arrays = split_data_for_models(generate_arrays(INDVARS_ARRAY_SIZE, ARRAYS_AMOUNT), NUMBER_OF_MODELS)
    for training_array in split_training_arrays:
        object_to_repr = repr_calc_in_a_set(training_array)
        objects_to_reprs_batch.append(object_to_repr)
    return objects_to_reprs_batch



def dump_models(trained_models: list[base.BaseEstimator]): 
    # getting the timestamp for the current machine learning model, saving it with this timestamp in the name
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    # Checking if the /trained_models folder exists, creating a new one if a folder of this name isn't found
    #models_foldername = 'trained_models'
    models_folder_path = Path(TRAINED_MODELS_PATH_NAME)
    try:
        #if not os.path.exists(models_folder_path):
        if not models_folder_path.exists():
            
            Path.mkdir(models_folder_path)
            print(f"Creating a folder for the trained models: {models_folder_path}")
    except:
        print("A problem occurred when trying to create a new folder ")
    print(f"trained_models: {trained_models}")
    
    # loop dumping the newest batch of trained models with timestamps and end numerators 
    # to differentiate between the models trained in the same batch
    for end_numerator in range(len(trained_models)):
        trained_model_path = models_folder_path.joinpath(f"model_{timestamp}_{end_numerator}.pkl")
        trained_model = trained_models[end_numerator]
        dump(trained_model, trained_model_path)
    
    












async def dummy_function():
    print("Dummy function started")
    await asyncio.sleep(20)
    print("Dummy function finished")

def dummy_task(task_id):

  start_time = datetime.now()
  print(f"Started task {task_id} on {start_time}")

  # Long process simulation
  sleep(10)

  end_time = datetime.now()
  print(f"Finished task {task_id} on {end_time}")

  return {
    "status": "Finished",
    "start_time": start_time.isoformat(),
    "end_time": end_time.isoformat(),
  }