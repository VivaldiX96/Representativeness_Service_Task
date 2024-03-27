from pydantic import BaseModel, validator

from parameters import NUMBER_OF_MODELS, IND_VARS_ARRAY_SIZE, ARRAYS_AMOUNT, K_NEAREST_NEIGHBOURS 




    
class NumberInput(BaseModel):
    number: float

    @validator('number')
    def number_must_be_in_range(cls, v):
        if v < 0 or v > 100:
            raise ValueError(f'The number must be in range from 0 to 100')
        return v

class NumbersInput(BaseModel):
    numbers: list[NumberInput]

    @validator('numbers')
    def validate_numbers_length(cls, v):
        if len(v) != IND_VARS_ARRAY_SIZE:
            raise ValueError(f'You should provide exactly {IND_VARS_ARRAY_SIZE} numbers')
        return v    