import yaml
from typing import Dict

class ConfigReader:

    def read(self, file_path: str) -> Dict:
        """Loads JSON configs into a dictionary."""
        with open(file_path) as user_configs:
            config = yaml.safe_load(user_configs)
            user_configs.close()
            return config

        #TODO: validate against json schema before returning data
        return None
