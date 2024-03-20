
from typing import List
from pydantic import BaseModel, confloat

class NumberList(BaseModel):
  numbers: List[float]  # Defining the inner list to hold independent variables

class DataPair(BaseModel):
  data: NumberList  # Use NumberList for the list of numbers
  value: float  # Define the single number

class DataList(BaseModel):
  data: List[DataPair]  # List of DataPair objects