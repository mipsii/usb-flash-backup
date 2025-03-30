import asyncio
from PySide6.QtCore import QMetaObject, Qt, QObject, Signal, QRunnable

class SignalManager(QObject):
    # Privatna promenljiva koja čuva instancu klase
    _instance = None  
    # Definicija signala
    analyze_files = Signal()
    history_changed = Signal(dict)
    upddate_gui = Signal(str)
    signal_gui = Signal(str, dict)
    send_merged_state = Signal(dict)
    analyze_files = Signal()
    usb_status_changed = Signal(str, dict)  # Signal sa serijskim brojem i detaljima o USB-u
    usb_event = Signal(str, str)  # Akcija, Serijski broj, Labela, Device node 
    finished_signal = Signal(object)

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SignalManager, cls).__new__(cls)  # Pravi instancu ako ne postoji
            cls._instance.__init__(*args, **kwargs)
            return cls._instance  # Vraća postojeću instancu
        
    def __init__(self):
        super().__init__()
        self._registered_methods = {}

    def connect_signal(self, signal_name, receiver, method_name):
        # Generičko povezivanje signala prema imenu signala i imenu metode
        signal = getattr(self, signal_name, None)
        if signal:
            method = getattr(receiver, method_name, None)
            if callable(method):
                signal.connect(method)

    def connect_signal_async(self, signal_name, receiver, method_name ):
        signal = getattr(self, signal_name, None)
        if signal:
            method = getattr(receiver, method_name, None)
            signal.connect(lambda: asyncio.create_task(method()))

    def emit_signal(self, signal_name, *args):
        # Generičko emitovanje signala prema imenu signala
        signal = getattr(self, signal_name, None)
        if signal:
            signal.emit(*args)
    
    
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

    def start_task(self, func, *args, **kwargs):
        worker = Worker(func, *args, **kwargs)
        worker.setAutoDelete(True)  # Automatski briše instancu nakon izvršavanja
        self.thread_pool.start(worker)  # Pokretanje u thread pool-u

    def start_thread(self, func, *args, tag=None, **kwargs):
        thread = WorkerThread(func, *args, **kwargs)
        
        # Povezivanje signala sa internim signalom ili tagom
        if tag:
            thread.finished_signal.connect(lambda result: self.emit_signal_by_tag(tag, result))
        else:
            thread.finished_signal.connect(self.thread_finished.emit)

        # Startovanje threada
        thread.start()
        self.thread._threads.append(thread)  # Čuvanje reference da nit ne bi bila uklonjena iz memorije


class Worker(QRunnable):
    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.func(*self.args, **self.kwargs)

from PySide6.QtCore import QThread, Signal, QObject, QMetaObject, Qt

class WorkerThread(QThread):

    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        result = self.func(*self.args, **self.kwargs)
        self.finished_signal.emit(result)
