from fastapi import FastAPI
from pydantic import BaseModel


# the integer parameters that will influence the scale of the model training task
class TrainingParameters(BaseModel):
    NumberOfModels: int
    Size: int
    ArraysAmount: int
    KNearestNeighbours: int
    