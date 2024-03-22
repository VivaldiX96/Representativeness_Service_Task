
from typing import List
from pydantic import BaseModel, confloat, validator


class VariablesRow(BaseModel):
    independentvars: List[float]  # Can change float to int depending on your data type
    dependentvar: float

class MachineLearningData(BaseModel):
    mldata: List[VariablesRow]

    @validator("data")
    def validate_data(cls, value: List[dict]) -> List[VariablesRow]:
        for pair in value:
            if not isinstance(pair, dict):
                raise ValueError("Invalid pair format. Each pair should be a dictionary.")
            if "independentvars" not in pair or "dependentvar" not in pair:
                raise ValueError("Missing 'numbers' or 'dependentvar' key in a pair.")
            if not isinstance(pair["numbers"], list):
                raise ValueError("'numbers' element should be a list of numbers.")
            if not isinstance(pair["dependentvar"], (int, float)):
                raise ValueError("'dependentvar' element should be a number.")
        return [VariablesRow(**pair) for pair in value]
