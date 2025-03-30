import os
import platform
from usb_manager_linux import USBManagerLinux
from usb_manager_windows import USBManagerWindows

class USBDeviceManager:
    def __init__(self, usb_class):
        super().__init__()
        self.usb_class = usb_class
        self.usb_info = self.usb_class.usb_info_manager.get_usb_info()
        self.os_name = platform.system()
        self.usb_manager = self._initialize_usb_manager()
        self.current_device = self.usb_class.usb_info_manager.get_current_usb_info()  # Ovde čuvamo trenutno prikazan uređaj
        
    def _initialize_usb_manager(self):
        if self.os_name == "Linux":
            return USBManagerLinux()
        elif self.os_name == "Windows":
            return USBManagerWindows()
        else:
            raise EnvironmentError("Nepodržan operativni sistem")

    def get_connected_usb_devices(self, device_node):
        # Logika za prepoznavanje svih USB uređaja
         
        if self.os_name == "Linux":
            device = self.usb_manager.get_usb_serial_linux(device_node)
            #print(f"od linux je { device}")
        elif self.os_name == "Windows":
            device = self.usb_manager.get_connected_usb_devices_windows(device_node)
        return device
    
    def mount_all_devices(self):
        devices = self.get_connected_usb_devices()
        for device in devices:
            self.usb_manager.mount_usb(device)
            print(f"Montiran uređaj: {device}")
            
    def find_device(self, device=None, serial_number=None, mount_point=None, label=None):
        """Pretraga uređaja prema određenim karakteristikama."""
        usb_info = self.usb_class.usb_info_manager.get_usb_info()
        for serial_info, info in usb_info.items():
            if (((device is None) or (info['Device']) == device) and
                ((serial_number is None) or (serial_info == serial_number)) and
                ((mount_point is None) or (info['Mount Point'] == mount_point)) and
                ((label is None) or (info['Label'] == label))):
                return serial_info, info  # Vraća prvi uređaj koji odgovara kriterijumima
        return None  # Vraća None ako nije pronađen nijedan uređaj
    
    def create_hidden_file_with_serial_number(self, folder_name, serial_number):
        """Kreira skriveni fajl sa serijskim brojem u datom folderu."""
        hidden_file_name = ".serial_number"
        folder_path = os.path.join(os.getcwd(), folder_name)
        if not os.path.exists(folder_path):
            print(f"Folder {folder_name} ne postoji.")
            return
        self.create_hidden_file(folder_path, hidden_file_name, serial_number)
        self.usb_class.json_files.save_json_data(os.path.join(folder_path, hidden_file_name), serial_number, 4)
        print(f"Skriveni fajl sa serijskim brojem {serial_number} je kreiran u {folder_path}.")
        

    def create_hidden_file(self, folder_path, hidden_file_name):
        if platform.system() == "Windows":
            os.system(f'attrib +h "{os.path.join(folder_path, hidden_file_name)}"')
