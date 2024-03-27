
from typing import List
from pydantic import BaseModel, validator

from parameters import IND_VARS_ARRAY_SIZE, MIN_INDEPENDENT_VARIABLE, MAX_INDEPENDENT_VARIABLE

# the integer parameters that will influence the scale of the model training task
# class TrainingParameters(BaseModel):
#     NumberOfModels: int
#     Size: int
#     ArraysAmount: int
#     KNearestNeighbours: int

    
class IndVariableInput(BaseModel):
    ind_var: float

    @validator('ind_var')
    def ind_var_must_be_in_range(cls, v):
        if v < MIN_INDEPENDENT_VARIABLE or v > MAX_INDEPENDENT_VARIABLE:
            raise ValueError(f'The independent variable must be in range from {MIN_INDEPENDENT_VARIABLE} to {MAX_INDEPENDENT_VARIABLE}')
        return v

class IndVariablesInput(BaseModel):
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
            raise ValueError(f"Dependent variable must be in range (0, 1). Value: {v}") #represetativeness can be only in range (0, 1)
        return v


class MachineLearningData(BaseModel):
    ml_data: List[VariablesRow]

class DepVariable(BaseModel):
    dep_var: float

