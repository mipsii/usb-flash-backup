import json
import os
import platform

class ConfigManager:
    _instance = None  # Privatni atribut za čuvanje jedne instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        # Proveravamo da li je instanca već inicijalizovana
        if not hasattr(self, '_initialized'):
            self._initialized = True
            
            # Postavlja putanju za konfiguracioni fajl na osnovu operativnog sistema
            self.os_type = platform.system().lower()
            if self.os_type == 'windows':  # Windows
                self.config_path = os.path.join(os.getenv('APPDATA'), "usb_backup_config.ini")
                
            elif self.os_type == 'linux':  # Linux/Mac
                self.config_path = os.path.expanduser("~/.config/usb_backup_config.ini")
               
            self.config = self.load_json_data()
                        
            # Sačuvaj OS tip u konfiguraciji
            self.save_config("os_type", self.os_type)
            
            
    def save_config(self, key, value):
        """Čuva serijski broj i putanju za backup u JSON fajlu."""
        self.config[key] = value
        self.save_json_data()
            
    def get_backup_config(self):
        return self.config.get("backup_base_path", None)
        
    def get_os_type(self):
        return self.config.get("os_type")  # koji sistem 

    def load_json_data(self):
        """Učitaj podatke iz JSON fajla, ako postoji."""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                return json.load(f)
        return {}

    def save_json_data( self):
        """Sačuvaj podatke u JSON fajl."""
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=4)