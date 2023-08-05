

class ConfigException(Exception):
    def __init__(self, key: str):
        message = f'Config value for key {key} could not be found '
        super().__init__(message)
