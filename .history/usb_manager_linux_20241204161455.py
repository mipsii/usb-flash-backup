import json
import subprocess

class USBManagerLinux:
    
    def __init__(self): 
        pass
      
    # def get_usb_info_linux(self, device_path):
    #     """
    #     Koristi `lsblk` za detekciju USB uređaja na Linuxu.
    #     """
    #     lsblk_data = self.get_lsblk()  # Pretpostavljamo da imate ovu metodu.
    #     for device in lsblk_data['blockdevices']:
    #         if device.get("tran") == "usb" and device.get("path") == device_path:
    #             serial_number = device.get('serial')
    #             mount_point = device.get('mountpoint')
    #             label = device.get('label')
    #             return device_path, mount_point, serial_number, label
    #     return None

      
    def get_usb_serial_linux(self, device_path):
        """Hvatanje serijskog broja USB uređaja i putanje na Linux-u."""
        """ trans - > usb :  name -> glavni uređaj (npr., 'sdb' za '/dev/sdb1') """
        try:
            if not self.is_mounted(device_path):
                self.mount_usb(device_path)
                
            atribut = self.get_path(device_path)
            # Koristimo lsblk za dobijanje informacija o uređaju
            lsblk_data = self.get_lsblk()
            # Prolazimo kroz sve uređaje u lsblk izlazu
            for device in lsblk_data['blockdevices']:
                if device[atribut] == device_path[:-1][-3:]:  # Pronađi glavni uređaj (npr., 'sdb' za '/dev/sdb1')
                    serial_number = device.get('serial')  # Uzimamo serijski broj glavnog uređaja
                    print(f"Serijaki {serial_number}")
                    # Ako je direktno montiran
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
                        print(f"postoji mountt {device_path, mount_point, label, serial_number}")
                        #USBDeviceManager.add_device_info(device_path, mount_point, label, serial_number) 
                        
                        return { 'Serial number': serial_number, 
                                'Label': label,
                                'Device': device_path,
                                'Mount Point': mount_point                                
                                }
                        
        except Exception as e:
            print(f"Greška pri čitanju serijskog broja ili mount pointa: {e}")
            return None, None, None, None
        
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
 
    def get_path(self, device_name):
        if device_name == "usb:":
                return "trans"
        else:
            return "name"

    def get_lsblk(self):
        lsblk_result = subprocess.run(['lsblk', '-J', '-o', 'TRAN,MOUNTPOINT,LABEL,SERIAL,NAME'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        lsblk_output = lsblk_result.stdout.decode('utf-8')
        return json.loads(lsblk_output)
    
    def mount_usb(self, device):
        try:
            full_device_path = device
            # Pokrenite mount komandu
            a = subprocess.run(['udisksctl', 'mount', '-b', full_device_path], check=True)
            print(f"USB uređaj {device} je uspešno montiran") 
            return
        except subprocess.CalledProcessError as e:
            print(f"Greška prilikom montiranja uređaja {device}: {e}")
            return
        
    def get_mount_and_label(self, device):
            mount_point = device.get('mountpoint')
            label = device.get('label')
            print(label)
            return mount_point, label
             

            
    