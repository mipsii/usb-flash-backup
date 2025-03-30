from PySide6.QtWidgets import QApplication,QWidget, QComboBox, QVBoxLayout, QLabel, QPushButton, QListWidget, QSplitter, QListWidgetItem, QMainWindow
from PySide6.QtCore import Qt

from signal_manager import SignalManager
from localization import _
from translation import TranslationManager

class UiGui:
    
    def __init__(self, main_windows):
        """Inicijalizuje GUI sa referencom na logičku klasu."""
        self.main_windows = main_windows  # Spremamo referencu na logičku klasu
        self.is_register_action = True
        self._signals()
        self.translation_manager = TranslationManager(self)

    def _signals(self):
        self.signal_manager = SignalManager()
        self.signal_manager.connect_signal("sigUsbStatusChanged", self, "update_usb_status")
        self.signal_manager.connect_signal("sigGui", self, "update_usb_status")   
       #self.signal_manager.connect_signal("sigRemoveUsb", self, "usb_remove") 
       
    """Klasa koja definiše korisnički interfejs."""
    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow  # Sačuvaj referencu na MainWindow
        #MainWindow.setWindowTitle(_("USB Backup"))
        self.translation_manager.add_widget(MainWindow, _("USB Backup"))
        MainWindow.resize(215, 170)
        self.MainWindow.setMinimumSize(0, 0)
    
        # Centralni widget i layout
        self.centralwidget = QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)
        self.vertical_layout = QVBoxLayout(self.centralwidget)

         # Dropdown za izbor jezika
        self.lang_selector = QComboBox()
        self.lang_selector.addItems([_("English"), _("Srpski"), _("Czesky")])
        #self.translation_manager.add_widget(self.lang_selector, [_("English"), _("Srbski"), _("Czesky")])
        self.lang_selector.currentIndexChanged.connect(self.change_language) 
        self.vertical_layout.addWidget(self.lang_selector)

        
        # QSplitter za horizontalno deljenje
        self.splitter = QSplitter(Qt.Horizontal)

         # Središnji deo
        self.middle_widget = QWidget(self.splitter)
        #self.middle_widget.setFixedWidth(195)
        self.middle_widget.setMaximumWidth(217)
        self.middle_layout = QVBoxLayout(self.middle_widget)

        # Glavna labela
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Status labela
        self.statusLabel = QLabel(self.centralwidget)
        self.statusLabel.setObjectName("statusLabel")
        self.statusLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Dugme koje će biti skriveno inicijalno
        self.changeButton = QPushButton("", self.centralwidget)
        self.changeButton.setObjectName("changeButton")

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
        self.changeButton.clicked.connect(self.decide_action)

        # Postavljanje početnih poruka preko metoda
        self.set_label_message( "USB nije umetnut")
        self.set_status_message("Whait", color = "gray")
        self.set_button_state("Promeni status", False)

        try:
            with open("styles.qss", "r") as f:
                style = f.read()
                print("Stil uspešno učitan!")
        except FileNotFoundError:
            print("Fajl 'style.qss' nije pronađen.")
        except Exception as e:
            print(f"Greška pri čitanju fajla: {e}")

        MainWindow.setStyleSheet(style)

    def change_language(self, index):
            # Mapiranje indeksa u jezike
            languages = {
                0: 'en',
                1: 'sr',
                2: 'cs'
            }
            new_language = languages.get(index)
            print(f"[izabao je ] .......{new_language}")
            self.signal_manager.emit_signal("sigChangeLanguage", new_language)            
        
    def set_status_message(self, message, color="white"):
        #self.statusLabel.setText(message)
        self.translation_manager.add_widget(self.statusLabel, _(message))
        self.statusLabel.setStyleSheet(f"color: {color};")

    def set_label_message(self, message, color="white"):
        self.translation_manager.add_widget(self.label, _(message))
        self.statusLabel.setStyleSheet(f"color: {color};")

    def set_button_state(self, text="", visible=True):
        self.translation_manager.add_widget(self.changeButton, _(text))
        self.changeButton.setVisible(visible)

    def toggle_left_widget(self, bool):
        """Prikaz/Sakrivanje levog dela."""
        self.left_widget.setVisible( bool)
        self.adjust_window_size()

    def toggle_right_widget(self, bool):
        """Prikaz/Sakrivanje desnog dela."""
        self.right_widget.setVisible(bool)
        self.adjust_window_size()

    def decide_action(self):
        print("dugme registarcija/backup je pritisnuto")
        self.signal_manager.emit_signal("sigUsbAction")

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
            self.set_label_message(_(f"USB: { usb['Label'] }"))
            self.set_status_message( _(f"USB je povezan na {usb['Device']}."))
            self.changeButton.setVisible(True)
        else:
            self.set_label_message( _(f"USB nije umetnut"))
            self.set_status_message("Whait")
            self.changeButton.setVisible(False)

    def usb_remove(self):
        # Uklanjanje informacija o USB-u
        # self.label.setText("")
        # self.translation_manager.add_widget( self.label, _("USB nije priključen"))
        # self.statusLabel.setText("")
        self.backup_list.clear()
        
        self.toggle_left_widget(False)
        print(f"levo krilo je ......{self.left_widget.isVisible()}")
        print(f"desno krilo je ......{self.right_widget.isVisible()}")
        if QApplication.instance().findChild(QMainWindow, "window"):
            self.main_windows.window.close()

   
    def update_usb_status(self, serial_number , usb):
        """Ažurira GUI u zavisnosti od statusa umetnutog USB-a."""
        print(f"........azurirrao listu u gui..........")
        if usb["Is current"]:
            self.label.setText("")
            self.translation_manager.add_widget(self.label, _(f"USB: { usb['Label']}"))
            #self.statusLabel.setText("USB je povezan.")
            self.changeButton.setVisible(True)

            if usb["Is registar"]:
                if usb["Active"]:
                    self.set_button_state(_("Backup"))
                    self.is_register_action = False
                    self.set_status_message(_("USB je registrovan. <br> Spreman za backup."), color='green')
                else:
                    self.changeButton.setVisible(False)
                    self.set_button_state("", False)
                    self.is_register_action = True
                    self.set_status_message(_("USB je registrovan. <br> nije aktivan."), "orange")
            else:   
                self.set_button_state( _("Registruj& mount USB"))
                self.set_status_message(_("USB nije registrovan. Registrujte ga."), "red")
        else:
            self.set_label_message(_("nema USB aktivnih"))
            self.set_status_message("")
            self.changeButton.setVisible(False)