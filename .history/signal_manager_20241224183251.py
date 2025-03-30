from PySide6.QtCore import Signal, QObject

class SignalManager(QObject):
    # Privatna promenljiva koja čuva instancu klase
    _instance = None  
    # Definicija signala
    signal_from_class_a = Signal()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SignalManager, cls).__new__(cls)  # Pravi instancu ako ne postoji
            cls._instance.__init__(*args, **kwargs)
            return cls._instance  # Vraća postojeću instancu
    def __init__(self):
        super().__init__()

    def connect_signals(self, receiver):
            # Povezivanje signala iz klase A sa metodom u receiveru (koji može biti iz bilo koje klase)
            self.signal_from_class_a.connect(receiver.receive_signal)
    
    def emit_signal(self, data):
        # Emitovanje signala
        self.signal_from_class_a.emit(data)