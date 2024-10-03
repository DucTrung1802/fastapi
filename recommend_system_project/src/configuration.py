import os

class Configuration:
    def __init__(self):
        pass
    
    def get_environment_variale(self, variable_name: str):
        return os.getenv(variable_name)