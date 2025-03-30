import platform
import subprocess
import time
from usbmonitor import USBMonitor
from usbmonitor.attributes import ID_MODEL, ID_MODEL_ID, ID_VENDOR_ID, ID_SERIAL
try:
    import wmi
except ImportError:
    wmi = None  # Provera za Windows
    
class USBDevice:
    def __init__(self, usb_info):
        self.usb_info = usb_info
        self.monitor = USBMonitor()
        print("Starting USBMonitor...")
        self.monitor.start_monitoring(on_connect=self.on_connect, on_disconnect=self.on_disconnect)

    def __repr__(self):
        return f"{self.device_name} ({self.serial_number}) mounted at {self.mount_point}"

    def on_connect(self, device_id, device_info):
        print(f"Device connected with ID: {device_info}")
        
        device_node = device_info.get('DEVNAME', 'N/A')
        serial_number = device_info.get(ID_SERIAL, 'N/A')
        device_name = device_info.get(ID_MODEL, 'N/A')
        mount_point = self.get_mount_point(device_node)
       
        print(f"Detected device node: {device_node}") 
        print(f"Serial number: {serial_number}") 
        print(f"Device name: {device_name}")
        
        if not mount_point:
            print(f"USB uređaj detektovan: {device_name} ({serial_number}). Montiranje je potrebno.")
            # Dodaj logiku za prikaz dugmeta za montiranje
            
        else:
            print(f"Connected: {self.usb_info}")
            # Logika kada je uređaj montiran
        self.add_device_info(device_node, mount_point, device_name, serial_number)
        
    def on_disconnect(self, device_id, device_info):
        device_node = device_info.get('DEVNAME', 'N/A')
        print(f"Disconnected: {device_node}")
        # Logika kada je uređaj odspojen
        print(f"Disconnected: {device_node}")

    def add_device_info(self, device_node, mount_point, device_name, serial_number):
        """Dodavanje USB uređaja u listu."""
        self.usb_info.append({
            'Device Name': device_node,
            'Mount Point': mount_point,
            'Label': device_name,
            'Serial Number': serial_number
        })

    def get_mount_point(self, device_node):
        """Funkcija za dobijanje tačke montiranja USB uređaja"""
        if platform.system() == "Linux":
            return self.get_mount_point_linux(device_node)
        elif platform.system() == "Windows":
            return self.get_mount_point_windows(device_node)
        else:
            raise EnvironmentError("Nepodržan operativni sistem")
        
    def get_mount_point_linux(self, device_node):
        try: 
            mounts = subprocess.check_output(['mount']).decode().split('\n')
            for mount in mounts:
                if device_node in mount:
                    return mount.split(' ')[2]
        except subprocess.CalledProcessError:
            return None
        return None

    def get_mount_point_windows(self, device_node):
        
        c = wmi.WMI()
        for disk in c.Win32_LogicalDisk():
            if disk.DeviceID == device_node:
                return disk.Caption
        return None

# Primer korišćenja
usb_devices = [] 
listener = USBDevice(usb_info=usb_devices)

while True: 
    time.sleep(1)