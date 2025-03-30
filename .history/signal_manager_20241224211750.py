from PySide6.QtCore import QMetaObject, Qt, QObject, Signal

class SignalManager(QObject):
    # Privatna promenljiva koja čuva instancu klase
    _instance = None  
    # Definicija signala
    analyze_files = Signal()
    history_changed = Signal(dict)

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
    
    def emit_signal(self, signal_name, *args):
        # Generičko emitovanje signala prema imenu signala
        signal = getattr(self, signal_name, None)
        if signal:
            signal.emit(*args)

    def register_async_method(self, receiver, method_name):
        self._registered_methods[method_name] = receiver

    def emit_invoke_method(self, method_name, *args):
        receiver = self._registered_methods.get(method_name, None)
        if receiver:
            QMetaObject.invokeMethod(receiver, method_name, Qt.QueuedConnection, *args)