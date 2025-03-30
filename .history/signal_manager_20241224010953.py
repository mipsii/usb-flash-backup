from PySide6.QtCore import Signal, QObject

class SignalManager(QObject):
    _instance = None  # Privatna promenljiva koja čuva instancu klase
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SignalManager, cls).__new__(cls)  # Pravi instancu ako ne postoji
            cls._instance.__init__(*args, **kwargs)
        return cls._instance  # Vraća postojeću instancu
