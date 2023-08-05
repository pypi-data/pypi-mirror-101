import os
import yaml
from typing import Dict
from exception import ConfigException


class Config:

    base_path: str
    config_dict: Dict

    def __init__(self, config_path: os.path):
        self.base_path = config_path
        config_files = self.__get_all_config_files_with_names()
        self.config_dict = self.__parse_config_files(config_files)

    def get(self, key: str, default=None):
        key_split = key.split('.')
        d_name, keys = key_split[0], key_split[1:]
        try:
            result = self.config_dict[d_name]
        except KeyError:
            if default is None:
                raise ConfigException(key)
            else:
                return default
        for k in keys:
            result = result.get(k, None)
            if result is None:
                if default is None:
                    raise ConfigException(key)
                else:
                    return default
        return result

    @staticmethod
    def __parse_config_files(config_files: Dict) -> Dict:
        cfg = {}
        for config_file_name, config_file_path in config_files.items():
            with open(config_file_path, 'r') as file:
                cfg[config_file_name] = yaml.safe_load(file)
        return cfg

    def __get_all_config_files_with_names(self) -> Dict:
        config_files = {}
        for name in os.listdir(self.base_path):
            current_path = os.path.join(self.base_path, name)
            if os.path.isfile(current_path):
                name_stripped = os.path.splitext(name)[0]
                config_files[name_stripped] = current_path
        return config_files
