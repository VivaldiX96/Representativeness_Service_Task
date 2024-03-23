
from typing import List
from pydantic import BaseModel, confloat, validator



# the integer parameters that will influence the scale of the model training task
# class TrainingParameters(BaseModel):
#     NumberOfModels: int
#     Size: int
#     ArraysAmount: int
#     KNearestNeighbours: int

class VariablesRow(BaseModel):
    indvars: List[float]  # independent variables
    depvar: float #dependent variable

class MachineLearningData(BaseModel):
    mldata: List[VariablesRow]


