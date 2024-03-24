from pathlib import Path
import os

# models_folder_name = Path('trained_models')
# models_folder_name = 'trained_models'

# os.makedirs(models_folder_name)
nd = Path("ndir_3")
nd.mkdir()
print("hello world")
print(nd.exists())