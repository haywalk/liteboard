from typing import Self, Any
import time
import yaml

CONFIG_FILE = './config.yml'

class Config:
    ''' Singleton database interface.
    '''
    _instance: Self = None
    config_data: dict

    def __new__(cls) -> Self:
        ''' Create config if it doesn't exist.
        '''
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.reload(CONFIG_FILE)

        return cls._instance
        
    def reload(self, config_file: str) -> None:
        ''' Reload the config.

        Args:
            config_file (str): Path to config file.
        '''
        with open(config_file, 'r', encoding='utf-8') as file:
            self.config_data = yaml.safe_load(file)

    def get(self, attribute: str, default: Any = None) -> Any:
        ''' Get a setting from the config.

        Args:
            attribute (str): Name of setting.
            default (Any): Default value if attribute is unset.

        Returns:
            Any: Value of setting.
        '''
        return self.config_data.get(attribute, default)

class Date:
    ''' Date utilities.
    '''
    @staticmethod
    def timestamp() -> str:
        ''' Get the current UNIX time.

        Returns:
            str: Current UNIX time (ms).
        '''
        return str(int(time.time() * 1000))