import json
import os
import subprocess
import pyudev


class UsbDetectManager:
    def __init__(self):
        pass
    
    
    def get_usb_info(self, device_path):
        try:
         
            # Koristimo lsblk za dobijanje informacija o uređaju
            lsblk_data = self.get_lsblk()
            # Prolazimo kroz sve uređaje u lsblk izlazu
            
            for device in lsblk_data['blockdevices']:     
    
                if device["tran"] =="usb":  # Pronađi glavni uređaj (npr., 'sdb' za '/dev/sdb1')
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
                            return device_path, mount_point, serial_number, label
        except Exception as e:
            print(f"Greška pri čitanju serijskog broja ili mount pointa: {e}")
            return None, None, None
    def get_lsblk(self):
        lsblk_result = subprocess.run(['lsblk', '-J', '-o', 'TRAN,MOUNTPOINT,LABEL,SERIAL,NAME'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        lsblk_output = lsblk_result.stdout.decode('utf-8')
        return json.loads(lsblk_output)
    def get_mount_and_label(self, device):
        mount_point = device.get('mountpoint')
        label = device.get('label')
        print(label)
        return mount_point, label
    def get_mount_point(self, device_path):
        """Pronađi tačku montiranja za zadati uređaj."""
        print(f" device path je   {device_path}")
        try:
            output = subprocess.run(
                ["lsblk", "-o", "NAME,MOUNTPOINT", "-n"],
                stdout=subprocess.PIPE, text=True
            )
            for line in output.stdout.splitlines():
                parts = line.split()
                print(f"parts:   {parts}")
                #print(f"parts:   {parts}")
                if parts[0] in device_path:  # Uklapa se sa uređajem
                    print(f"parts:   {parts}")
                    return parts[2] if len(parts) > 1 else None  # Mont point ili None
        except Exception as e:
            print(f"Greška pri dobavljanju tačke montiranja: {e}")
        return None
    
# Testiranje
manager = UsbDetectManager()
usb_info = manager.get_usb_info("/dev/sdb1")
print("Pronađeni USB uređaji:")
print(usb_info)
