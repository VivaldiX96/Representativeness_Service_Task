
from typing import List
from pydantic import BaseModel, validator

from parameters import NUMBER_OF_MODELS, IND_VARS_ARRAY_SIZE, ARRAYS_AMOUNT, K_NEAREST_NEIGHBOURS 

# the integer parameters that will influence the scale of the model training task
# class TrainingParameters(BaseModel):
#     NumberOfModels: int
#     Size: int
#     ArraysAmount: int
#     KNearestNeighbours: int

    
class IndVariableInput(BaseModel):
    """
     A float that must be in range (0, 100). Independent variable that machine learning data will be comprised of.
    """
    ind_var: float

    @validator('ind_var')
    def ind_var_must_be_in_range(cls, v):
        if v < 0 or v > 100:
            raise ValueError(f'The independent variable must be in range from 0 to 100')
        return v

class IndVariablesInput(BaseModel):
    """
    List of independent variables of given length, set with a constant variable IND_VARS_ARRAY_SIZE in the parameters.py file.
    """
    ind_vars: list[float]

    @validator('ind_vars', check_fields=False)
    def validate_variables_length(cls, v):
        if len(v) != IND_VARS_ARRAY_SIZE:
            raise ValueError(f'You should provide exactly {IND_VARS_ARRAY_SIZE} variables')
        return v    

class VariablesRow(BaseModel):
    ind_vars: List[float] # independent variables
    dep_var: float #dependent variable

    @validator("dep_var")
    def validate_dep_var(cls, v: float) -> float:
        if v < 0 or v > 1:
            raise ValueError(f"Dependent variable must be in range (0, 1). Value: {v}")
        return v


class MachineLearningData(BaseModel):
    ml_data: List[VariablesRow]

class DepVariable(BaseModel):
    dep_var: float

