import json
import os
import platform
import subprocess
from utils.json_file import save_json_data

class USBSerialManager:
    def __init__(self, usb_info):
        self.usb_info = usb_info
        
    def add_device_info(self, device, mount_point, label, serial_number):
            """Dodavanje USB uređaja u listu."""
            self.usb_info.append({
                'Device Name': device,
                'Mount Point': mount_point,
                'Label': label,
                'Serial Number': serial_number
        })

    def find_device(self, name=None, serial_number=None, mount_point=None, label=None):
        """Pretraga uređaja prema određenim karakteristikama."""
        for info in self.usb_info:
            if ((name is None or info['Device'] == name) and
                (serial_number is None or info['Serial Number'] == serial_number) and
                (mount_point is None or info['Mount Point'] == mount_point) and
                (label is None or info['Label'] == label)):
                return info  # Vraća prvi uređaj koji odgovara kriterijumima
        return None  # Vraća None ako nije pronađen nijedan uređaj
    
    def is_usb_mounted_linux(self):
        try:
            result = subprocess.check_output(["lsblk", "-o", "MOUNTPOINT,NAME"])
            if "usb" in result.decode('utf-8').lower():
                return True
        except subprocess.CalledProcessError:
            return False
        return False

    def get_usb_serial(self):
        """Detektuje serijski broj USB-a u zavisnosti od OS-a."""
        if platform.system() == "Windows":
            return self.get_usb_serial_windows()
        elif platform.system() == "Linux":
            return self.get_usb_serial_linux()
        else:
            print("Nepoznat sistem")
            return None, None, None

    def get_usb_serial_windows(self):
        """Hvatanje serijskog broja USB uređaja na Windows-u."""
        import wmi
        c = wmi.WMI()
        usb_devices = []
        for usb in c.Win32_DiskDrive():
            if "USB" in usb.Caption:
                usb_devices.append(usb)
        return usb_devices

    def get_mount_point_by_serial_windows(self, serial_number):
        """Vraća montiranu putanju za USB sa datim serijskim brojem."""
        import win32api  # Importuje se samo na Windows-u
        usb_devices = self.get_usb_serial_windows()
        
        usb_devices = win32api.GetLogicalDriveStrings().split('\000')[:-1]
        
        for drive in usb_devices:
            if win32api.GetDriveType(drive) == win32api.DRIVE_REMOVABLE:
                for usb_serial, device_id in usb_devices:
                    if serial_number in device_id:
                        return serial_number, drive
        return None, None
    
    def get_usb_serial_linux(self, device_path):
        """Hvatanje serijskog broja USB uređaja i putanje na Linux-u."""
        """ trans - > usb :  name -> glavni uređaj (npr., 'sdb' za '/dev/sdb1') """
        try:
            if not self.is_mounted(device_path):
                self.mount_usb(device_path)
                
            atribut = self.get_path(device_path)
            print(atribut)
            # Koristimo lsblk za dobijanje informacija o uređaju
            lsblk_data = self.get_lsblk()
            # Prolazimo kroz sve uređaje u lsblk izlazu
            for device in lsblk_data['blockdevices']:
                if device[atribut] == device_path[:-1][-3:]:  # Pronađi glavni uređaj (npr., 'sdb' za '/dev/sdb1')
                    serial_number = device.get('serial')  # Uzimamo serijski broj glavnog uređaja
                    print(f"Serijaki {serial_number}")
                    # Ako je direktno montiran
                    print("pred pitanje")
                    mount_point = device.get('mountpoint')
                    print(mount_point)
                    mount_point = device.get('mountpoint')
                    print(mount_point)
                    label = device.get('label')
                    print(f"label je {label}")
                   
                    if 'children' in device:
                    # Prolazimo kroz sve particije (children)
                        for partition in device['children']:
                            if partition.get('mountpoint'):
                                # Ako je pronađena odgovarajuća montirana particija
                                mount_point, label =  self.get_mount_and_label(partition)
                    if mount_point :
                        self.add_device_info(device, mount_point, label, serial_number) 
                              
             # Ispisujemo prikupljene informacije
            for info in self.usb_info:
                #print(f"Device: {info['Device']}, Mount Point: {info['Mount Point']}, Label: {info['Label']}, Serial Number: {info['Serial Number']}")
                if info['Mount Point']:
                    return info['Serial Number'], info['Mount Point'], info['Label'] 
                    #return 5, 6 , 7
                else:
                    # Ako ništa nije pronađeno, vraćamo None 
                    return None, None, None
                
        except Exception as e:
            print(f"Greška pri čitanju serijskog broja ili mount pointa: {e}")
            return None, None, None

    def get_path(self, device_name):
        if device_name == "usb:":
                return "trans"
        else:
            return "name"
    
    def get_lsblk(self):
        lsblk_result = subprocess.run(['lsblk', '-J', '-o', 'TRAN,MOUNTPOINT,LABEL,SERIAL,NAME'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        lsblk_output = lsblk_result.stdout.decode('utf-8')
        return json.loads(lsblk_output)
    
    def get_mount_and_label(self, device):
            mount_point = device.get('mountpoint')
            label = device.get('label')
            print(label)
            return mount_point, label
    
    def is_mounted(self, device):
        try:
            # Provera montiranih tačaka za uređaj pomoću lsblk
            result = subprocess.check_output(["lsblk", "-o", "MOUNTPOINT", device]).decode("utf-8")
            mountpoints = result.splitlines()[1:]  # Preskačemo prvi red jer je naslov
            # Ako postoji montpoint (nije prazan string), uređaj je montiran
            return any(mountpoint.strip() for mountpoint in mountpoints)
        except subprocess.CalledProcessError as e:
            print(f"Greška prilikom provere montiranog uređaja: {e}")
            return False
           
    def mount_usb(self, device):
        try:
            full_device_path = device
            # Pokrenite mount komandu
            a = subprocess.run(['udisksctl', 'mount', '-b', full_device_path], check=True)
            print(f"USB uređaj {device} je uspešno montiran") 
            return 
            
        
        except subprocess.CalledProcessError as e:
            print(f"Greška prilikom montiranja uređaja {device}: {e}")
            
    def create_hidden_file_with_serial_number(self, folder_name, serial_number):
        """Kreira skriveni fajl sa serijskim brojem u datom folderu."""
        hidden_file_name = ".serial"
        folder_path = os.path.join(os.getcwd(), folder_name)
        if not os.path.exists(folder_path):
            print(f"Folder {folder_name} ne postoji.")
            return
        self.create_hidden_file(folder_path, hidden_file_name, serial_number)
        save_json_data(os.path.join(folder_path, hidden_file_name), serial_number, 4)
        print(f"Skriveni fajl sa serijskim brojem {serial_number} je kreiran u {folder_path}.")
        

    def create_hidden_file(self, folder_path, hidden_file_name):
        if platform.system() == "Windows":
            os.system(f'attrib +h "{os.path.join(folder_path, hidden_file_name)}"')
            
            
if __name__ == "__main__":
    usb_manager = USBSerialManager()
    usb = usb_manager.get_usb_serial_linux("sdb")

    if usb['Serial Number']:
        print(f"Serijski broj USB-a: {usb['Serial Number']} \nmount je: {usb['Mount Point']} \nime je : {usb['Label']}")
    else:
        print("USB uređaj nije detektovan ili serijski broj nije pronađen.")
           
