"""Storage module"""

import pickle
from pathlib import Path

class Storage:
    """Storage class"""

    DEFAULT_STORAGE_PATH = "./storage"

    def __init__(self):
        try:
            path = Path(self.DEFAULT_STORAGE_PATH)
            path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise e
        self.storage_path = path

    def save_data(self, serialization_object, filename: str):
        '''Serialize object to storage'''

        with open(self.storage_path.joinpath(filename), "wb") as f:
            pickle.dump(serialization_object, f)

    def load_data(self, filename: str):
        '''Deserialize object from storage'''

        try:
            with open(self.storage_path.joinpath(filename), "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return None
