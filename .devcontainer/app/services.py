
from datetime import datetime

from pathlib import Path
import os
import random

import joblib
import numpy as np
from joblib import dump
from models import VariablesRow, MachineLearningData, IndVariablesInput, DepVariable

from sklearn import base

from parameters import NUMBER_OF_MODELS, IND_VARS_ARRAY_SIZE, ARRAYS_AMOUNT, K_NEAREST_NEIGHBOURS
import math

TRAINED_MODELS_PATH_NAME = 'trained_models' # name of a folder created (once) for all the trained models

STATUS_FILE_NAME = "latest_training_status"


        
async def check_training_status():
    """
    Function for the endpoint that enables checking the current status of execution of the recently started training
    by reading the current contents of the text file latest_training_status.txt generated by the train_models function.

    """
    current_dir = Path.cwd()
    status_file_name = STATUS_FILE_NAME
    status_file_path = Path(os.path.join(current_dir, status_file_name))
    try:
        # Read status from file using 'with' for automatic closing
        with status_file_path.open('r') as status_file:
            current_training_status_message = status_file.read()
    except FileNotFoundError:
        current_training_status_message = "Training hasn't started yet."
    return current_training_status_message




def generate_arrays(array_size: int, 
                          #number of arrays must be above a number that provides 
                          #enough examples to train the model but is not excessively high
                          arrays_amount: int):
    """
    Function generating a set of arrays of the chosen size 'size' with arrays_amount elements;
    It returns a list of arrays of random numbers to be used as independent variables in ML training
    """

    # Initialize an empty list to store the generated arrays
    arrays = []
    
    # Loop over the specified number of arrays to generate
    for i in range(arrays_amount):
        # Generate an array of size 'size' comprising of numbers from 0 to 100
        array = [random.uniform(0, 100) for _ in range(array_size)]
        
        # Add the generated array to the list of arrays
        arrays.append(array)
    
    return arrays


def split_data_for_models(training_arrays, PartsNumber: int): #maybe change PartsNumber to local variable?
    """
    Function takes the training_arrays list of training arrays generated by generate_arrays,
    and splits it randomly into NUMBER_OF_MODELS (= "L" value from the task description), keeping the order of the numbers in individual lists
    """
    # Create and shuffle indices
    indices = list(range(len(training_arrays)))
    random.shuffle(indices)

    # Split data using shuffled indices
    split_data = [[] for _ in range(PartsNumber)]
    for i, idx in enumerate(indices):
        split_data[i % PartsNumber].append(training_arrays[idx])
  
    split_data = [training_arrays[i::PartsNumber] for i in range(PartsNumber)]
    
    return split_data



def repr_calc_in_a_set(objects: list):
    """
    Function calculating representativeness values for all the objects in a given list
    and filling a dict of the calculated repr. values for each object
    """

    #For each object, calculating distances from all other objects
    sublist_size = len(objects)
    ml_data_items = [] # dictionary of pairs object : representativeness, with the size of the sublist taken by the function
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
        dep_var = 1 / (1 + avg_distance) #dependent variable being the calculated representativeness
         
        # appending the representativeness value to a list of objects mapped to their repr. values
        ml_data_items.append(VariablesRow(ind_vars=obj, dep_var=dep_var)) #appending mutable elements in order to enable optional feature scaling later
    #print(f"list of representativeness:") # optional line for checking the values
    #print(ml_data_items) # for value checking/program observation
    return MachineLearningData(ml_data=ml_data_items)

async def generate_data():
    """
    function generating dummy training data to be copied to the /train-models endpoint
    """
    objects_to_reprs_batch = []
    split_training_arrays = split_data_for_models(generate_arrays(IND_VARS_ARRAY_SIZE, ARRAYS_AMOUNT), NUMBER_OF_MODELS)
    for training_array in split_training_arrays:
        object_to_repr = repr_calc_in_a_set(training_array)
        objects_to_reprs_batch.append(object_to_repr)
    return objects_to_reprs_batch


def dump_models(trained_models: list[base.BaseEstimator]): 
    """
    Function saves the model as .pkl in a special folder (creates the folder if it didn't exist before)
    """
    # getting the timestamp for the current machine learning model, saving it with this timestamp in the name
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    # Checking if the /trained_models folder exists, creating a new one if a folder of this name isn't found
    models_folder_path = Path(TRAINED_MODELS_PATH_NAME)
    try:
        #if not os.path.exists(models_folder_path):
        if not models_folder_path.exists():
            
            Path.mkdir(models_folder_path)
            print(f"Creating a folder for the trained models: {models_folder_path}")
    except:
        print("A problem occurred when trying to create a new folder ")
    
    # loop dumping the newest batch of trained models with timestamps and end numerators 
    # to differentiate between the models trained in the same batch
    
    for end_numerator in range(len(trained_models)): # len(trained_models) == NUMBER_OF_MODELS from the moment the training started.
        trained_model_path = models_folder_path.joinpath(f"model_{timestamp}_{end_numerator}.pkl")
        trained_model = trained_models[end_numerator]
        dump(trained_model, trained_model_path)
    
    
async def get_recent_models():
    """
    Function that gets the recent batch of trained models. The number of the models in one batch is defined globally - not editable by the User
    """

    models_filenames = os.listdir("trained_models")
    print(models_filenames) #OK, works
    models_filepaths: Path = []
    for model_filename in models_filenames:
        model_path = os.path.join("trained_models", model_filename)
        models_filepaths.append(model_path)
        #models_filepaths.append(model_filename)
    # Sorting the files based on the time of modification
    models_filepaths.sort(key=os.path.getmtime, reverse=True)
    

    # Loading the recently trained group of models
    predicting_models = []
    for i in range(NUMBER_OF_MODELS):
        print(f"model filepath to grab number {i}: {models_filepaths[i]}")
        model_to_grab = joblib.load(models_filepaths[i])
        predicting_models.append(model_to_grab)
    #print(f"predicting_models: {predicting_models}")  # optional line for checking
    return predicting_models


async def predict_from_models_array(raw_ind_vars_for_prediction:  list[IndVariablesInput]): 
    """
    Function that makes a new prediction from a set of new independent variables
    """
    predictions = []
    ind_vars_for_prediction = []

    for single_raw_ind_vars_list in raw_ind_vars_for_prediction:
        single_ind_vars_list = single_raw_ind_vars_list.ind_vars
        ind_vars_for_prediction.append(single_ind_vars_list)


    models = await get_recent_models()
    print(models)
    predicted_values_sum = 0
    for single_ind_vars_list in ind_vars_for_prediction:
        for model in models:
            #print(f"supplied array X:{np.array(single_ind_vars_list).reshape(1, -1)}") # optional line for checking
            
            predicted_value: float = model.predict(np.array(single_ind_vars_list).reshape(1, -1))
            
            predicted_values_sum += predicted_value
        average_prediction: float = predicted_values_sum / NUMBER_OF_MODELS
        #print(f"Average prediction: {average_prediction}") # optional line for checking
        predictions.append(DepVariable(dep_var=average_prediction))
    return predictions

