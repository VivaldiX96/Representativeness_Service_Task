
from sklearn.ensemble import RandomForestRegressor


NUMBER_OF_MODELS: int = 4    # "L" from task description - Default number of parts into which we split 
                             # the whole group of training arrays; also the number of models
                             # from which the averaged prediction will be obtained.
                             # It is _not_ directly editable by the User

IND_VARS_ARRAY_SIZE: int = 5  # Default size of one array of numbers that will become a single row 
                             # of independent variables in the training data; not editable by the User


K_NEAREST_NEIGHBOURS: int = 3 # the number of the nearest neighbours of each analyzed object - 
                          # this number will influence the representativeness analysis

N_ESTIMATORS: int = 10 #number of estimators that is set for each regression model

# This value makes it possible to generate more or less training data to be delivered to the regression model for it's training
ARRAYS_AMOUNT: int = 40  # Total number of arrays of numbers (each of the size = SIZE) 
                         # on which the model will be initially trained

