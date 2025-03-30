from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QSplitter,QListWidgetItem,QFrame, QHBoxLayout
from PySide6.QtCore import Qt

class UiGui:
    def __init__(self, main_windows):
        """Inicijalizuje GUI sa referencom na logičku klasu."""
        self.main_windows = main_windows  # Spremamo referencu na logičku klasu
        
    """Klasa koja definiše korisnički interfejs."""
    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow  # Sačuvaj referencu na MainWindow
        MainWindow.setWindowTitle("USB Backup")
        MainWindow.resize(215, 170)
        self.MainWindow.setMinimumSize(0, 0)
        
        # Centralni widget i layout
        self.centralwidget = QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)
        self.vertical_layout = QVBoxLayout(self.centralwidget)
        
        # QSplitter za horizontalno deljenje
        self.splitter = QSplitter(Qt.Horizontal)

         # Središnji deo
        self.middle_widget = QWidget(self.splitter)
        #self.middle_widget.setFixedWidth(195)
        self.middle_widget.setMaximumWidth(217)
        self.middle_layout = QVBoxLayout(self.middle_widget)

        # Glavna labela
        self.label = QLabel("USB nije umetnut", self.centralwidget)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Status labela
        self.statusLabel = QLabel("", self.centralwidget)
        self.statusLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Dugme koje će biti skriveno inicijalno
        self.changeButton = QPushButton("Promeni status", self.centralwidget)
        self.changeButton.setVisible(False)

        self.middle_layout.addWidget(self.label)
        self.middle_layout.addWidget(self.statusLabel)
        self.middle_layout.addWidget(self.changeButton)     

        # Leva strana
        self.left_widget = QWidget(self.splitter)
        self.left_layout = QVBoxLayout(self.left_widget)
        #self.left_widget.setFixedWidth(155)
        self.left_widget.setStyleSheet("background-color: #404066;")

        # Dodavanje liste za backup-ove
        self.backup_list = QListWidget(self.left_widget)
        self.left_layout.addWidget(self.backup_list)
        
        # Desna strana
        self.right_widget = QWidget(self.splitter)
        self.right_layout = QVBoxLayout(self.right_widget)
        #self.right_widget.setFixedWidth(200)
        self.right_widget.setStyleSheet("background-color: blue;")
        self.right_label = QLabel("Desni deo", self.right_widget)
        self.command_files = QListWidget(self.right_widget)
        self.right_layout.addWidget(self.right_label)

        # Dodavanje QSplitter u glavni layout
        self.vertical_layout.addWidget(self.splitter)

        # Početno sakrivanje levog i desnog prozora
        self.left_widget.setVisible(False)
        self.right_widget.setVisible(False)

        try:
            with open("styles.qss", "r") as f:
                style = f.read()
                print("Stil uspešno učitan!")
        except FileNotFoundError:
            print("Fajl 'style.qss' nije pronađen.")
        except Exception as e:
            print(f"Greška pri čitanju fajla: {e}")

        MainWindow.setStyleSheet(style)

    def set_status_message(self, message, color="black"):
        self.statusLabel.setText(message)
        self.statusLabel.setStyleSheet(f"color: {color};")

    def set_button_state(self, text="", visible=True):
        self.changeButton.setText(text)
        self.changeButton.setVisible(visible)

    def toggle_left_widget(self, bool):
        """Prikaz/Sakrivanje levog dela."""
        self.left_widget.setVisible( bool)
        self.adjust_window_size()

    def toggle_right_widget(self, bool):
        """Prikaz/Sakrivanje desnog dela."""
        self.right_widget.setVisible(bool)
        self.adjust_window_size()

    def adjust_window_size(self):
        """Prilagođavanje širine i centriranje prozora."""
        # Početna širina središnjeg dela
        width = 200  # Širina središnjeg dela bez dodataka
        # Dodaj širinu za vidljive delove
        if self.left_widget.isVisible():
            width += 212  # Širina levog dela
        if self.right_widget.isVisible():
            width += 222  # Širina desnog dela

        # Postavi novu veličinu prozora
        current_geometry = self.MainWindow.geometry()
        print(f" nova geeometrija .....{ current_geometry } i  .... { width}")
        self.MainWindow.resize(width, current_geometry.height())

    def usb_inserted(self, serial_number, usb):
        print("usao je u ui instert") 
        print(f"povrtane inf serijski { serial_number}  i  info  {usb['Label']}")
        if serial_number:
            self.label.setText(f"USB: { usb['Label'] } Serijski broj: { serial_number }")
            self.statusLabel.setText(f"USB je povezan na {usb['Device']}.")
            self.changeButton.setVisible(True)
        else:
            self.label.setText(f"USB nije umetnut")
            self.statusLabel.setText(f"")
            self.changeButton.setVisible(False)

    def usb_remove(self, serial_number):
        # Uklanjanje informacija o USB-u
        self.label.setText("USB nije priključen")
        self.statusLabel.setText("")
        self.backup_list.clear()
        
        self.toggle_left_widget(False)
        print(f"levo krilo je ......{self.left_widget.isVisible()}")
        print(f"desno krilo je ......{self.right_widget.isVisible()}")

    def update_backup_list_widget(self, backups):
        """Ažurira prikaz liste backup-ova."""
        self.backup_list.clear()  # Briše prethodni sadržaj
        print(f" ....update_backup_list_widget stiglo je .....{backups}")
        # Obrni listu backupova (najnoviji prvi)
        #reversed_backups = list(reversed(backups["backup_history"]))
        backup_path = backups["backup_path"]  # Preuzmi putanju
        
        for index, backup in reversed(list(enumerate(backups["backup_history"]))):
            formatted_backup = self.main_windows.ui_logic.format_backup_datetime(backup)  # Poziv metode iz Logic klase
            item = QListWidgetItem(formatted_backup)  # Kreira novi element za svaki backup
            item.setData(Qt.UserRole, index)
            item.setData(Qt.UserRole + 1, backup_path)
            print(f" index j e .... {item.data(Qt.UserRole)}")
            self.backup_list.addItem(item)
    
    def update_usb_status(self, serial_number , usb):
        """Ažurira GUI u zavisnosti od statusa umetnutog USB-a."""
        if usb["Is current"]:
            self.label.setText(f"USB: { usb['Label']} <br> (Serijski broj: {serial_number})")
            self.statusLabel.setText("USB je povezan.")
            self.changeButton.setVisible(True)

            if usb["Is registar"]:
                if usb["Active"]:
                    self.changeButton.setText("Backup")
                    self.statusLabel.setStyleSheet("color: green;")
                    self.statusLabel.setText("USB je registrovan. <br> Spreman za backup.")
                else:
                    self.changeButton.setVisible(False)
                    self.statusLabel.setStyleSheet("color: orange;")
                    self.statusLabel.setText("USB je registrovan. <br> nije aktivan.")
            else:
                self.changeButton.setText("Registruj USB")
                self.statusLabel.setStyleSheet("color: red;")
                self.statusLabel.setText("USB nije registrovan. Registrujte ga.")
        else:
            self.label.setText("USB nije priključen")
            self.statusLabel.setText("")
            self.changeButton.setVisible(False)