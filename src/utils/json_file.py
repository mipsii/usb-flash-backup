import json
import os

from config import ConfigManager

class JsonFileManager:
    def __init__(self):
        self.config_manager = ConfigManager()
        
    def load_json_data(self,file_path):
        """Učitaj podatke iz JSON fajla, ako postoji."""
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return json.load(f)
        return {}

    def save_json_data(self, file_path, data, indent_level=4):
        """Sačuvaj podatke u JSON fajl."""
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=indent_level)

    def get_backup_path_from_config(self):
        return  self.config_manager.get_backup_config()
        
    def get_os(self):
        config = self.load_json_data(os.path.exists("usb_backup_config.ini"))
        return config["os_type"]

