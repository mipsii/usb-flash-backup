from PySide6.QtCore import Signal, QObject

class SignalManager(QObject):
    # Privatna promenljiva koja čuva instancu klase
    _instance = None  
    # Definicija signala
    signal_from_class_a = Signal()
    analyze_files = Signal()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SignalManager, cls).__new__(cls)  # Pravi instancu ako ne postoji
            cls._instance.__init__(*args, **kwargs)
            return cls._instance  # Vraća postojeću instancu
    def __init__(self):
        super().__init__()

    # def connect_signals(self, receiver):
    #         # Povezivanje signala iz klase A sa metodom u receiveru (koji može biti iz bilo koje klase)
    #         self.signal_from_class_a.connect(receiver.receive_signal)
    
    # def emit_signal(self, data):
    #     # Emitovanje signala
    #     self.signal_from_class_a.emit(data)

    def connect_signal(self, signal_name, receiver, method_name):
        # Generičko povezivanje signala prema imenu signala i imenu metode
        signal = getattr(self, signal_name, None)
        if signal:
            method = getattr(receiver, method_name, None)
            if callable(method):
                signal.connect(method)
    
    def emit_signal(self, signal_name, data=None):
        # Generičko emitovanje signala prema imenu signala
        signal = getattr(self, signal_name, None)
        if signal:
            signal.emit(data)
