import json
from os import path
import tempfile

class Configuration():

    def __init__(self, name = 'config.json'):
        self._name = path.join(tempfile.gettempdir(), name)

    
    def read(self):
        if not path.exists(self._name):        
            return {}

        with open(self._name) as file:
            return json.load(file)
        

    def write(self, data: dict[str, str]):
        with open(self._name, 'w') as file:
            json.dump(data, file)

