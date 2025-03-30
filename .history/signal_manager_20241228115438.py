import asyncio
import traceback
from PySide6.QtCore import QMetaObject, Qt, QObject, Signal

class SignalManager(QObject):
    # Privatna promenljiva koja čuva instancu klase
    _instance = None  
    # Definicija signala
    analyze_files = Signal()
    history_changed = Signal(dict)
    upddate_gui = Signal(str)
    signal_gui = Signal(str, dict)
    send_merged_state = Signal(dict)
    usb_status_changed = Signal(str, dict)  # Signal sa serijskim brojem i detaljima o USB-u
    usb_action =Signal()
    backup_signal =Signal()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SignalManager, cls).__new__(cls)  # Pravi instancu ako ne postoji
            cls._instance.__init__(*args, **kwargs)
        return cls._instance  # Vraća postojeću instancu
        
    def __init__(self):
        if not hasattr(self, "_initialized"):  # Sprečava ponovno pozivanje __init__
            super().__init__()
            self._initialized = True  # Obeležava da je inicijalizacija već izvršena
            print("SignalManager kreiran")
        self._registered_methods = {}

    def connect_signal(self, signal_name, receiver, method_name):
        # Generičko povezivanje signala prema imenu signala i imenu metode
        signal = getattr(self, signal_name, None)
        if signal:
            method = getattr(receiver, method_name, None)
            if callable(method):
                #print(f"[CONNECT-ASYNC] Signal: {signal_name} -----> {receiver}.{method_name}")
                print(f"[CONNECT-ASYNC] Signal: {signal_name} -----> {method.__name__}")
                #print("Traceback (odakle se povezuje slot):")
                #print(''.join(traceback.format_stack(limit=5)))
                signal.connect(method)

    def connect_signal_async(self, signal_name, receiver, method_name):
        signal = getattr(self, signal_name, None)
        if signal:
            method = getattr(receiver, method_name, None)
            if callable(method):
                #print(f"[CONNECT-ASYNC] Signal: {signal_name} -----> {receiver}.{method_name}")
                print(f"[CONNECT-ASYNC] Signal: {signal_name} -----> {method}")
                #print("Traceback (odakle se povezuje slot):")
                #print(''.join(traceback.format_stack(limit=5)))
                # Pravljenje asinhronog zadatka sa prosleđenim argumentima
                signal.connect(lambda  *args: asyncio.create_task(method(*args)))
            
    def emit_signal(self, signal_name, *args):
        # Generičko emitovanje signala prema imenu signala
        print(f"[EMIT] Signal: {signal_name} | Data: {args}")
        signal = getattr(self, signal_name, None)
        if signal:
            signal.emit(*args)
        else:
            print(f"Signal {signal_name} nije pronađen!")

    # Registracija metode pod određenim tagom
    def register_async_method(self, receiver, method_name, tag):
        if tag not in self._registered_methods:
            self._registered_methods[tag] = []
        self._registered_methods[tag].append((receiver, method_name))

    # Pozivanje svih metoda koje su registrovane pod istim tagom
    def emit_invoke_method_by_tag(self, tag, *args):
        if tag in self._registered_methods:
            for receiver, method_name in self._registered_methods[tag]:
                if not QMetaObject.invokeMethod(receiver, method_name, Qt.QueuedConnection, *args):
                    print(f"Failed to invoke method {method_name} on {receiver}")
        else:
            print(f"No tag registered with name '{tag}'")

    def unregister_async_method(self, tag, receiver, method_name):
        if tag in self._registered_methods:
            self._registered_methods[tag] = [
                (r, m) for r, m in self._registered_methods[tag]
                if not (r == receiver and m == method_name)
        ]

    # Pregled Svih Slotova (Ručno Pokretanje Analize)
    def list_connected_signals(self):
        for signal_name in dir(self):
            signal = getattr(self, signal_name)
            if isinstance(signal, Signal):
                print(f"[CHECK] Signal: {signal_name}")
                print(signal)
                print(signal.receivers())  # Lista svih povezanih slotova

    