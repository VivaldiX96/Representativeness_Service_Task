from fastapi import FastAPI
from pydantic import BaseModel, Field, validator
from typing import List
from parameters import NUMBER_OF_MODELS, INDVARS_ARRAY_SIZE, ARRAYS_AMOUNT, K_NEAREST_NEIGHBOURS 




    
class NumberInput(BaseModel):
    number: float

    @validator('number')
    def number_must_be_in_range(cls, v):
        if v < 0 or v > 100:
            raise ValueError(f'The number must be in range from 0 to 100')
        return v

class NumbersInput(BaseModel):
    numbers: List[NumberInput]

    @validator('numbers')
    def validate_numbers_length(cls, v):
        if len(v) != INDVARS_ARRAY_SIZE:
            raise ValueError(f'You should provide exactly {INDVARS_ARRAY_SIZE} numbers')
        return v    