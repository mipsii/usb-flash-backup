import sys
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton,QStatusBar,QApplication, QListWidget, QTabWidget, QHBoxLayout

class BackupPopup (QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Pregled promena za backup")
        self.resize(400, 300)

        # Glavni layout
        layout = QVBoxLayout(self)
        
        # Kreiraj TabWidget
        self.tab_widget = QTabWidget(self)

        # Tab za nove fajlove
        self.new_files_tab = self._create_file_list_tab("Novi fajlovi:")
        self.tab_widget.addTab(self.new_files_tab, "Novi")

        # Tab za obrisane fajlove
        self.deleted_files_tab = self._create_file_list_tab("Obrisani fajlovi:")
        self.tab_widget.addTab(self.deleted_files_tab, "Obrisani")

        # Tab za izmenjene fajlove
        self.modified_files_tab = self._create_file_list_tab("Izmenjeni fajlovi:")
        self.tab_widget.addTab(self.modified_files_tab, "Izmenjeni")

        # Dodaj TabWidget u glavni layout
        layout.addWidget(self.tab_widget)

        # Donji layout za dugmad
        button_layout = QHBoxLayout()
        self.backup_button = QPushButton("Pokreni backup", self)
        self.cancel_button = QPushButton("Otkaži", self)
        button_layout.addStretch()  # Raspoređuje dugmad desno
        button_layout.addWidget(self.backup_button)
        button_layout.addWidget(self.cancel_button)

        # Povezivanje dugmadi sa akcijama
        self.cancel_button.clicked.connect(self.reject)  # Zatvara popup
        self.backup_button.clicked.connect(self.accept)  # Prihvata akciju

        # Dodaj dugmad u glavni layout
        layout.addLayout(button_layout)

    def _create_file_list_tab(self, label_text):
        """Pomoćna funkcija za kreiranje taba sa listom fajlova."""
        tab = QVBoxLayout()
        label = QLabel(label_text, self)
        file_list = QListWidget(self)  # Lista fajlova
        tab.addWidget(label)
        tab.addWidget(file_list)
        container = QDialog(self)  # Omotavanje layouta u QDialog za TabWidget
        container.setLayout(tab)
        return container

if __name__ == "__main__":
    app = QApplication(sys.argv)
    popup = BackupPopup()
    if popup.exec() == QDialog.DialogCode.Accepted:
        print("Backup pokrenut!")
    else:
        print("Backup otkazan.")
    sys.exit(app.exec())