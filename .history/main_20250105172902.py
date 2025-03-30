import asyncio
import gettext
from PySide6.QtWidgets import QMainWindow, QApplication
import pyudev
from file_change import FileChangeManager
from file_collector import FileCollector
from signal_manager import SignalManager
from ui_gui import UiGui
from ui_logic import UiLogic
from file_explorer_view import MmainWindow

class MainWindow(QMainWindow):
   
    def __init__(self, usb_class):
        super().__init__()
        self.usb_class = usb_class
        
        # Inicijalizacija korisničkog interfejsa
        self.ui_gui = UiGui(self)
        self.ui_gui.setupUi(self)
        self.ui_logic = UiLogic(self)
        self.file_collector = FileCollector()
        self.history = {}
        #self.check_connected_usb_devices()
        print("u main u je ")
        self._signals()
        
        
    def _signals(self):
        self.signal_manager = SignalManager() 
        self.signal_manager.connect_signal("sigHistoryChanged", self, "on_history_changed")
        self.signal_manager.connect_signal_async("sigUpDateGui", self, "file_change_method")
        self.signal_manager.connect_signal("sigFinished", self, "dd")
        self.signal_manager.connect_signal("sigGui", self, "signal_gui")
        self.signal_manager.connect_signal("sigSendMergedState",self, "manipulation_usb")

    def load_translation(self, lang_code):
        lang = gettext.translation('app', localedir='locale', languages=[lang_code], fallback=True)
        lang.install()
        global _
        _ = lang.gettext

    def dd(self):
        print("------------------------------------")
        print(f"lista je ------------- {self.file_collector.merged_state}")
        print("------------------------------------")
        self.window = MmainWindow(self.file_collector.merged_state)
        self.window.show()
        self.window.raise_()

    def handle_usb_event(self, action, deviceID):
        """Rukuje događajem umetanja ili uklanjanja USB-a."""
        print(f"promena sa  usb ..... {action} ..... { deviceID}")
        if action == "add":
            device = self.usb_class.usb_device.get_connected_usb_devices(deviceID)
            print(f".... uvucen hje  .....  {device}")
            # Preuzimanje informacija o uređaju na osnovu serijskog broja
            serial_number = device["Serial number"]
            # Provera da li je uređaj registrovan
            if device:
                print(f"......device je ....{device}")
            
            print("...pROVERA DA LI JE REGISTROVAN")
            #self.signal_manager.emit_signal("reg_or_backup_signal",serial_number, device)
            if  not serial_number in self.usb_class.usb_info:
                print("USB uređaj nije registrovan. Pokrećem registraciju.")
                # Registracija USB uređaja
                usb_label = device.get("Label")
                #self.usb_class.usb_folder.create_usb_folder(usb_label, serial_number)
                self.usb_class.add_usb_info(serial_number, device.get(("Label")), deviceID, 
                                        device.get("Mount Point"), 
                                        register_bool = False)
                # Dodavanje informacija u `usb_info`
                print(f"USB uređaj {serial_number} je sada registrovan.")
            else:
                # Ako je uređaj već registrovan, ažuriraj informacije
                print(f"USB uređaj {serial_number} je već registrovan. Ažuriram podatke.")
                self.usb_class.update_usb_info(serial_number, {'Device': deviceID})
                self.usb_class.update_usb_info(serial_number, {'Mount Point': device.get("Mount Point")})

            self.usb_class.update_usb_info(serial_number, {'Is current':True})
            self.usb_class.update_usb_info(serial_number, {'Active' :True})
            # Ažuriranje GUI-ja
            mount = device.get("Mount Point")
            print(f"....usbinfo je ...{self.usb_class.usb_info}")
            try:
                #loop = asyncio.get_running_loop()
                asyncio.create_task(self.analyz_files(serial_number, mount))
            except RuntimeError as e:
                print(f"Greška: asyncio petlja nije aktivna - {e}")
           
        elif action == "remove":
            # Uklanjanje informacija o USB-u
            device = self.usb_class.usb_device.find_device(device = deviceID)
            print(f"....usbinfo je ...{self.usb_class.usb_info}")
            print(f".....Izvadoio se ....{device}")
            if device:
                serial_number,_ = device
                print(f"usb je izvuceno i serijski je  {serial_number}")
                #asyncio.create_task(self.file_change.clear_changes())
                if self.file_change.popup is not None:
                    self.file_change.popup.reject()
                    #asyncio.create_task(self.file_change.clear_changes())
                    self.file_change.popup = None  # Resetuje referencu
                    print("USB je uklonjen. Popup zatvoren.")
                self.ui_gui.usb_remove()
                self.usb_class.usb_info_manager.remove_device(serial_number)
            else:
                print("laznjak")
        #self.signal_manager.emit_signal("seigUsbStatusChanged", serial_number, self.usb_class.usb_info[serial_number])
        print(f"....erijski broj pre update gui ...{serial_number}")
        self.signal_gui(serial_number)

    async def analyz_files(self, sserial_number, usb_backup = None):
        print("usao je u ......-------analyz_file")
        backup_path = self.usb_class.usb_folder.find_usb_folder(sserial_number)

        self.file_change_method(sserial_number, usb_backup)
        self.file_change = FileChangeManager( backup_path, usb_backup )
        print(f"kreiran file_change")
        
        self.signal_manager.emit_signal("sigAnalyzeFiles")
        #await self.file_change.analyze_changes()       

    def file_change_method(self, sserial_number, usb_backup = None):
        backup_path = self.usb_class.usb_folder.find_usb_folder(sserial_number)
        self.file_change = FileChangeManager( backup_path, usb_backup )

    def signal_gui(self, serial_number):
        print(f"usao u def signal gui i salje signal ")
        self.signal_manager.emit_signal("sigUsbStatusChanged", serial_number, self.usb_class.usb_info[serial_number])

    def on_history_changed(self, history):
        self.history = history
        print(f"history je ,.... {self.history}")

    def check_connected_usb_devices(self):
        """
        Proverava trenutno priključene USB uređaje i dodaje ih u listu uređaja.
        """
        print(f" proverava jel ima prikljucenih ")
        try:
            context = pyudev.Context()
            for device in context.list_devices(subsystem='block', DEVTYPE='partition'):
                # Proveri da li je USB uređaj
                if 'usb' in device.device_path:
                    device_path = device.device_node  # Npr., '/dev/sdb1'
                    self.handle_usb_event("add", device_path)
        except Exception as e:
            print(f"Greška pri proveri priključenih USB uređaja: {e}")

    def backup_files_index(self, backup_path, target):
         # Dobijanje aktuelnog event loop-a
        print(f"%%%backup_files_index%%%   ...  putanja je { backup_path}  a index je  {target} ")
        print(f"fajl history je ..... {self.history}")
        asyncio.create_task(self.file_collector.prenos(backup_path, self.history["backup_history"], target))

    def closeEvent(self, event):
        """Kada se zatvori glavni prozor, zatvori i sve pomoćne prozore."""
        if QApplication.instance().findChild(QMainWindow, "window"):
            self.main_windows.window.close()
        event.accept()

    def manipulation_usb(self):
        serial_number, details = self.usb_class.usb_info_manager.get_current_usb_info()

        if details["Is registar"]:
            self.signal_manager.emit_signal("sigBackup")
        else:
            print("REGISTRACIJA USB-a")
            label = details["Label"]
            self.usb_class.usb_folder.create_usb_folder(label, serial_number)
            self.usb_class.usb_info_manager.update_usb_info(serial_number, {"Is registar": True})
            self.signal_manager.emit_signal("usb_status_changed", serial_number, details)
    # def closeEvent(self, event):
    #     """Sakrij prozor sa task bara kada se klikne X."""
    #     event.ignore()
    #     self.hide()
        
    # Ovde možete dodati dodatne funkcionalnosti, poput prikazivanja notifikacije u tray-u
   
# Pokretanje aplikacije
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow("hjsj")
    window.show()
    app.exec()