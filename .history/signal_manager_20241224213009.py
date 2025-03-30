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

    # Registracija metode sa dodatnim tagom
    def register_async_method(self, receiver, method_name, tag=None):
        key = (method_name, tag)
        if key not in self._registered_methods:
            self._registered_methods[key] = []
        self._registered_methods[key].append(receiver)

    # Emitovanje sa opcionalnim tagom
    def emit_invoke_method(self, method_name, *args, tag=None):
        key = (method_name, tag)
        receivers = self._registered_methods.get(key, [])
        
        if not receivers:
            print(f"No method registered with name '{method_name}' and tag '{tag}'")
            return
        
        # Pozovi samo one sa odgovarajućim tagom
        for receiver in receivers:
            QMetaObject.invokeMethod(receiver, method_name, Qt.QueuedConnection, *args)