# usb_listener.py
import platform
import sys
from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets  import QApplication

class UsbListener(QThread):
    usb_event = Signal(str, str)  # Akcija, Device node

    def __init__(self, usb_class):
        super().__init__()  # Poziva konstruktor nadklase QObject
        self.usb_class = usb_class
        # Detekcija operativnog sistema
        self.os_type = platform.system().lower()

        if self.os_type == "linux":
            self.listener = UsbListenerLinux()
        elif self.os_type == "windows":
            import wmi
            self.listener = UsbListenerWindows()
        else:
            raise Exception("Unsupported OS")

        # Povezivanje signala sa odgovarajućom akcijom
        self.listener.usb_event.connect(self.usb_event.emit)

        self.run()
        
    def run(self):
        """Pokreće detekciju USB uređaja na osnovu sistema."""
        print('pokrece slusanje')
        self.listener.run()


import pyudev
class UsbListenerLinux(QThread):
    usb_event = Signal(str, str)  # Akcija, Serijski broj, Labela, Device node 
      
    def run(self):
        context = pyudev.Context()
        print("usao je u run contetx")  
        self.connected_devices = set()  # Set za praćenje trenutno povezanih uređaja
        monitor = pyudev.Monitor.from_netlink(context)
        monitor.filter_by('block')
              
        def usb_event(action, device):
             # Proverava akciju i tip uređaja pre emitovanja
            # Proverava samo događaje `add` i `remove`
            serial_number = device.get('ID_SERIAL')        
            print(f"serijski broj je  { serial_number }")    
            if device.device_node.endswith('1'):
                if action  == 'add':
                    print(f"Device attributes: {device}")

                    if not provera(serial_number):
                        print(f"Novi xsmidslo je   { device.device_node }")
                        self.connected_devices.add(serial_number)  # Dodaj uređaj u set
                        print(f"urdjaj je {self.connected_devices}")
                        self.usb_event.emit(action, device.device_node)
                    else:
                        print("ponavlja se ")
                        return
                elif action == "remove":
                    print(f"Uklonjen uređaj: {device.device_node}")
                    if  provera(serial_number):
                        print("brisemo ga iz evidencije")
                        self.connected_devices.discard(serial_number)  # Ukloni uređaj iz seta
                        self.usb_event.emit(action, device.device_node)
                    else:
                        print("ponavlja se ")
                        return
                                        
        observer = pyudev.MonitorObserver(monitor, usb_event)
        observer.daemon=True # enable CTRL+C for aborting
        observer.start()
        
        def provera(serial_number):
            if serial_number in self.connected_devices:
                print(f"Uređaj sa serijskim brojem {serial_number} je već registrovan.")
                return  True
            else:
                return False # Ako je uređaj već registrovan, ne šaljemo signal
           
# usb_listener_windows.py
class UsbListenerWindows(QThread):
    def __init__(self):
        import USBMonitor
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

    def get_mount_point_windows(self, device_node):
        
        c = wmi.WMI()
        for disk in c.Win32_LogicalDisk():
            if disk.DeviceID == device_node:
                return disk.Caption
        return None
    
    def run(self):
        import wmi
        wmi_obj = wmi.WMI()
        watcher = wmi_obj.watch_for(
            notification_type="Creation", wmi_class="Win32_USBHub"
        )

        while True:
            usb = watcher()
            serial_number = usb.DeviceID
            label = usb.Name
            device_node = usb.PNPDeviceID

            # Emituje signal sa detaljima USB-a i "add" akcijom
            self.usb_event.emit("add", serial_number, label, device_node)
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Kreirajte UsbListener objekat
    usb_listener = UsbListener()

    # Povezivanje signala sa metodom za obradu
    #usb_listener.usb_event.connect(usb_listener.handle_usb_event)

    # Pokrećemo thread
    usb_listener.start()

    sys.exit(app.exec())