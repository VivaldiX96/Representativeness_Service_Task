import random
from pydantic import BaseModel, confloat

async def generate_arrays(size: int, num_arrays: int(ge=100, le=10000)):
    """
    Generates a set of arrays of the chosen size 'size' with num_arrays elements.

    Parameters:
    - size (int): The size of each array in elements.
    - num_arrays (int): The number of arrays to generate.

    Returns: A list of arrays, where each array is a sequence of size 'size' filled with random numbers.
    """ 
    # Initialize an empty list to store the generated arrays
    arrays = []
    
    # Loop over the specified number of arrays to generate
    for i in range(num_arrays):
        # Generate an array of size 'size' comprising of numbers from 0 to 1000
        array = [random.uniform(0, 1000) for _ in range(size)]
        
        # Add the generated array to the list of arrays
        arrays.append(array)
    
    return arrays


#async def calculate_representativeness():
#