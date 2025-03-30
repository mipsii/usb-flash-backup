import os
import shutil
from PySide6.QtWidgets import (
    QDialog, QTabWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QListWidget, QApplication, QStatusBar, QListWidgetItem
)
from PySide6.QtCore import Qt, Signal, QThread
from PySide6 import QtCore
import sys
from localization import _
from translation import TranslationManager 

class ModernBackupPopup(QDialog):
    
    def __init__(self, modified_files=None, new_files=None, deleted_files=None, parent=None):
        super().__init__(parent)

        self.modified_files = modified_files or []  # Lista izmenjenih fajlova
        self.new_files = new_files or []           # Lista novih fajlova
        self.deleted_files = deleted_files or []   # Lista obrisanih fajlova
        self.translation_manager = TranslationManager(self)
        self.setWindowTitle(_("Pregled promena za backup"))
        self.resize(333, 300)

        # Primena modernog stila
        self.setStyleSheet("""
             QDialog {
                background-color: #2E3440;  /* Tamna pozadina */
                color: #D8DEE9;           /* Svetli tekst */
                border-radius: 10px;
            }
            QLabel {
                font-size: 14px;
                margin-bottom: 5px;
                color: #ECEFF4;           /* Svetliji tekst za bolju vidljivost */
            }
            QTabWidget::pane {
                border: 1px solid #4C566A;  /* Siva boja okvira */
                border-radius: 8px;
                padding: 5px;
            }
            QTabBar::tab {
                background: #4C566A;       /* Tamno siva pozadina */
                color: #ECEFF4;           /* Svetli tekst */
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
            QTabBar::tab:selected {
                background: #88C0D0;      /* Plava za selektovani tab */
                color: #2E3440;
            }
            QListWidget {
                background: #3B4252;       /* Tamna pozadina za listu fajlova */
                border: 1px solid #4C566A;
                border-radius: 5px;
                color: #D8DEE9;           /* Svetli tekst za stavke u listi */
                padding: 1px;
            }
            QPushButton {
                background-color: #5E81AC; /* Svetlo plava dugmad */
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #81A1C1; /* Svetlija nijansa na hover */
            }
            QPushButton:pressed {
                background-color: #4C566A; /* Tamnija nijansa kada se pritisne */
            }
            QProgressBar {
                border: 1px solid #4C566A;
                border-radius: 5px;
                text-align: center;
                background: #3B4252;       /* Tamna pozadina */
                color: #ECEFF4;           /* Svetli tekst za procenat */
            }
            QProgressBar::chunk {
                background: #5E81AC;       /* Plava boja za napredak */
                border-radius: 5px;
            }
            QListWidget::item {
                padding: 0px;  /* Ukloni padding */
                margin: 0px;   /* Ukloni marginu */
            }
        """)
        
        # Primer liste fajlova
        modified_files_list = QListWidget(self)
        new_files_list = QListWidget(self)
        deleted_files_list = QListWidget(self)
        
        #load lists
        modified_files_list = self._load_list(modified_files_list, self.modified_files)
        new_files_list = self._load_list(new_files_list, self.new_files)
        deleted_files_list = self._load_list(deleted_files_list, self.deleted_files)
        
        # Glavni layout
        layout = QVBoxLayout(self)

        # Kreiraj TabWidget
        self.tab_widget = QTabWidget(self)

        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet("color: white;")
        #self.status_bar.showMessage(_(""))
        self.translation_manager.add_widget(self.status_bar, "Prilagođeni status bar")
        
         # Tab za izmenjene fajlove
        self.modified_files_tab = self._create_file_list_tab(_("Izmenjeni fajlovi:"), modified_files_list )
        self.tab_widget.addTab(self.modified_files_tab, _("Izmenjeni"))
        
        # Tab za nove fajlove
        self.new_files_tab = self._create_file_list_tab(_("Novi fajlovi:"), new_files_list)
        self.tab_widget.addTab(self.new_files_tab, _("Novi"))

        # Tab za obrisane fajlove
        self.deleted_files_tab = self._create_file_list_tab(_("Obrisani fajlovi:"), deleted_files_list)
        self.tab_widget.addTab(self.deleted_files_tab, _("Obrisani"))

        # Dodaj TabWidget u glavni layout
        layout.addWidget(self.tab_widget)

        # Donji layout za dugmad
        button_layout = QHBoxLayout()
        self.cancel_button = QPushButton("", self)
        self.backup_button = QPushButton("Pokreni backup", self)
        self.translation_manager.add_widget(self.cancel_button, "Otkaži")
        self.translation_manager.add_widget(self.backup_button, "Pokreni backup")

        button_layout.addStretch()
        button_layout.addWidget(self.backup_button)
        button_layout.addWidget(self.cancel_button)

        layout.addWidget(self.status_bar)

        # Povezivanje dugmadi sa akcijama
        self.cancel_button.clicked.connect(self.reject)
        self.backup_button.clicked.connect(self.accept)

        # Dodaj dugmad u glavni layout
        layout.addLayout(button_layout)
    
    def _load_list(self, list, files):
        list.setIconSize(QtCore.QSize(0, 0))  # Importujte QtCore ako već nije

        for file in files:
                file_name = file.split("/")[-1]
                print(f"filename { file_name }")
                item = QListWidgetItem(file_name)
                item.setData(1, file)  # Skladištenje pune putanje u stavku
               
                self._on_mouse_move(item)
               
                list.addItem(item)
        return list
    
    def _on_mouse_move(self, item):
        file_path = item.data(1)  # Dohvatanje pune putanje iz stavke
        # Formatiranje za višelinijski prikaz
        max_length = 50  # Dužina svakog reda
        if len(file_path) > max_length:
            formatted_path = "<br>".join([file_path[i:i + max_length] for i in range(0, len(file_path), max_length)])
        else:
            formatted_path = file_path
        
        # Postavljanje HTML formatiranog tooltip-a
        item.setToolTip(f"<html><pre>{formatted_path}</pre></html>")
     
    def _create_file_list_tab(self, label_text, file_list):
        """Pomoćna funkcija za kreiranje taba sa listom fajlova."""
        tab = QVBoxLayout()
        
        label = QLabel(label_text, self)
        label.setAlignment(Qt.AlignLeft)

        tab.addWidget(label)
        tab.addWidget(file_list)
        
        container = QDialog(self)
        container.setLayout(tab)
        return container
            
    def reject(self):
        print("Backup proces je otkazan.")
        super().reject()  # Zatvori popup bez pokretanja backup-a
        return super().reject()
    
    def accept(self):
        return super().accept()

class BackupWorker(QThread):
    progress_updated = Signal(int)
    backup_completed = Signal(str)
    backup_failed = Signal(str)

    def __init__(self, new_files, deleted_files, modified_files, backup_path):
        super().__init__()
        self.new_files = new_files
        self.deleted_files = deleted_files
        self.modified_files = modified_files
        self.backup_path = backup_path

    def run(self):
        try:
            total_tasks = len(self.new_files) + len(self.deleted_files) + len(self.modified_files)
            completed_tasks = 0

            # Backup novih fajlova
            for file in self.new_files:
                source_path = file
                dest_path = os.path.join(self.backup_path, os.path.basename(file))
                shutil.copy2(source_path, dest_path)
                completed_tasks += 1
                self.progress_updated.emit(int((completed_tasks / total_tasks) * 100))

            # Brisanje fajlova
            for file in self.deleted_files:
                backup_file_path = os.path.join(self.backup_path, os.path.basename(file))
                if os.path.exists(backup_file_path):
                    os.remove(backup_file_path)
                completed_tasks += 1
                self.progress_updated.emit(int((completed_tasks / total_tasks) * 100))

            # Ažuriranje izmenjenih fajlova
            for file in self.modified_files:
                source_path = file
                dest_path = os.path.join(self.backup_path, os.path.basename(file))
                shutil.copy2(source_path, dest_path)
                completed_tasks += 1
                self.progress_updated.emit(int((completed_tasks / total_tasks) * 100))

            self.backup_completed.emit("Backup je uspešno završen!")
        except Exception as e:
            self.backup_failed.emit(f"Greška tokom backup procesa: {e}")
            
if __name__ == "__main__":
   # Primer podataka za testiranje
    modified_files = ["file1.txt", "file2.jpg", "file3.pdf"]
    new_files = ["new1.docx", "new2.xlsx"]
    deleted_files = ["old1.mp3", "old2.zip"]

    # Kreiranje aplikacije
    app = QApplication(sys.argv)

    # Inicijalizacija popup-a sa test podacima
    popup = ModernBackupPopup(
        modified_files=modified_files,
        new_files=new_files,
        deleted_files=deleted_files
    )

    if popup.exec() == QDialog.DialogCode.Accepted:
        print("Backup pokrenut!")
    else:
        print("Backup otkazan.")
    sys.exit(app.exec())
