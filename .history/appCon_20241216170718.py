#from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QSplitter,QListWidgetItem
from PySide6.QtCore import Qt, QRect

from usb_list import USBListManager

class Ui_USBBackup:
    """Klasa koja definiše korisnički interfejs."""
    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow  # Sačuvaj referencu na MainWindow
        MainWindow.setWindowTitle("USB Backup")
        MainWindow.resize(200, 170)
        self.MainWindow.setMinimumSize(0, 0)
        
        # Centralni widget i layout
        self.centralwidget = QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)
        self.vertical_layout = QVBoxLayout(self.centralwidget)
        
        # QSplitter za horizontalno deljenje
        self.splitter = QSplitter(Qt.Horizontal)

         # Središnji deo
        self.middle_widget = QWidget(self.splitter)
        self.middle_widget.setFixedWidth(165)
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
        self.left_widget.setFixedWidth(155)
        self.left_widget.setStyleSheet("background-color: #d2ebff;")
        # Dodavanje liste za backup-ove
        self.backup_list = QListWidget(self.left_widget)
        self.left_layout.addWidget(self.backup_list)
        
        # Desna strana
        self.right_widget = QWidget(self.splitter)
        self.right_layout = QVBoxLayout(self.right_widget)
        #self.right_widget.setFixedWidth(200)
        self.right_widget.setStyleSheet("background-color: blue;")
        self.right_label = QLabel("Desni deo", self.right_widget)
        self.right_layout.addWidget(self.right_label)

        # Dodavanje QSplitter u glavni layout
        self.vertical_layout.addWidget(self.splitter)

        # # Dugmad za prikazivanje/sakrivanje levog i desnog prozora
        # self.toggleLeftButton = QPushButton("Prikaži/Sakrij Levo", self.centralwidget)
        # self.toggleLeftButton.clicked.connect(self.toggle_left_widget)
        # self.toggleRightButton = QPushButton("Prikaži/Sakrij Desno", self.centralwidget)
        # self.toggleRightButton.clicked.connect(self.toggle_right_widget)

        # # Dodavanje dugmadi u središnji deo
        # self.middle_layout.addWidget(self.toggleLeftButton)
        # self.middle_layout.addWidget(self.toggleRightButton)
        
        # Početno sakrivanje levog i desnog prozora
        self.left_widget.setVisible(False)
        self.right_widget.setVisible(False)

    def toggle_left_widget(self):
        """Prikaz/Sakrivanje levog dela."""
        self.left_widget.setVisible(not self.left_widget.isVisible())
        self.adjust_window_size()

    def toggle_right_widget(self):
        """Prikaz/Sakrivanje desnog dela."""
        self.right_widget.setVisible(not self.right_widget.isVisible())
        self.adjust_window_size()

    def adjust_window_size(self):
        """Prilagođavanje širine i centriranje prozora."""
        # Početna širina središnjeg dela
        width = 200  # Širina središnjeg dela bez dodataka

        # Dodaj širinu za vidljive delove
        if self.left_widget.isVisible():
            width += 155  # Širina levog dela
        if self.right_widget.isVisible():
            width += 222  # Širina desnog dela

        # Postavi novu veličinu prozora
        current_geometry = self.MainWindow.geometry()
        print(f" nova geeometrija .....{ current_geometry } i  .... { width}")
        self.MainWindow.setFixedSize(width, current_geometry.height())

        # Centriraj prozor na osnovu trenutne pozicije
        # screen_geometry = QApplication.primaryScreen().geometry()
        # x = (screen_geometry.width() - width) // 2
        # y = current_geometry.y()  # Zadrži trenutnu visinu prozora
        # self.MainWindow.move(x, y)
         # Lista priključenih USB uređaja
        #self.usbList = QListWidget(MainWindow)
        # self.usbList.setFixedHeight(15)  # Ograničavamo visinu na prikaz 2-3 uređaja
        # self.usbList.setVisible(False)
        # self.usbList.setStyleSheet("font-family: 'Courier New'; font-size: 14px;")
        #self.usbList = self.usb_list_widget  # Dodeljivanje usb_list_widget koji je prosleđen
        #self.vertical_layout.addWidget(self.usbList)  # Dodaj usb listu u layout
        # Dodajemo elemente u layout
            
    def update_backup_list(self, backups):
        """Ažurira listu backup-ova u levom widget-u."""
        self.backup_list.clear()  # Briše prethodni sadržaj
        if backups:
            self.left_widget.setVisible(True)
        else:
            self.left_widget.setVisible(False)

        for backup in backups:
            item = QListWidgetItem(backup)  # Kreira novi element za svaki backup
            self.backup_list.addItem(item)
            
    def usb_inserted(self, serial_number, usb):
        print("usao je u handle") 
        print("add")
        print(f"u insert usb jee { usb }")
        print(f"povrtane inf serijski { serial_number}  i  info  {usb['Label']}")
        print(f"usb info je : { usb }")
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
        self.changeButton.setVisible(False)
        self.left_widget.setVisible(False)
        self.adjust_window_size()
        print(f"levo krilo je ......{self.left_widget.isVisible()}")
        print(f"desno krilo je ......{self.right_widget.isVisible()}")
        
                    
    def update_usb_status(self, serial_number , usb):
        """Ažurira GUI u zavisnosti od statusa umetnutog USB-a."""
        if usb["Is current"]:
            self.label.setText(f"USB: { usb['Label']} (Serijski broj: {serial_number})")
            self.statusLabel.setText("USB je povezan.")
            self.changeButton.setVisible(True)

            if usb["Is registar"]:
                self.changeButton.setText("Backup")
                self.statusLabel.setStyleSheet("color: green;")
                self.statusLabel.setText("USB je registrovan. Spreman za backup.")
            else:
                self.changeButton.setText("Registruj USB")
                self.statusLabel.setStyleSheet("color: red;")
                self.statusLabel.setText("USB nije registrovan. Registrujte ga.")
        else:
            self.label.setText("USB nije priključen")
            self.statusLabel.setText("")
            self.changeButton.setVisible(False)
        
    # def closeEvent(self, event):
    #     """Sakrij prozor sa task bara kada se klikne X."""
    #     event.ignore()
    #     self.hide()
    
   