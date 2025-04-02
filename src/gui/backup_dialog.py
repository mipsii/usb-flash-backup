# backup_dialog.py
import sys
import os
from PySide6.QtWidgets import QFileDialog, QApplication, QMessageBox, QInputDialog

class BackupDialog:
    def __init__(self):
        self.app = QApplication(sys.argv)

    
   
    def show_info_message(self, text, title="Informacija"):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setText(text)
        msg_box.setWindowTitle(title)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        return msg_box.exec()

    def show_warning_message(self, text, title="Upozorenje"):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setText(text)
        msg_box.setWindowTitle(title)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        return msg_box.exec()

    def show_question_message(self, text, title="Pitanje"):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Question)
        msg_box.setText(text)
        msg_box.setWindowTitle(title)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        return msg_box.exec()
    
    def show_critical_message(self, text, title="Critical"):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setText(text)
        return 

    def choose_backup_directory(self):
        while True:
            dialog = QFileDialog()
            dialog.setFileMode(QFileDialog.FileMode.Directory)
            dialog.setOption(QFileDialog.Option.ShowDirsOnly, True)
            folder_selected = dialog.getExistingDirectory(None, "Choose backup directory")

            if folder_selected:
                result = self.show_question_message("Do you want to create a new folder in the selected directory?")

                if result == QMessageBox.StandardButton.Yes:
                    new_folder, ok = QInputDialog.getText(None, "New Folder", "Enter new folder name:")
                    if ok and new_folder:
                        return self.create_new_folder(folder_selected, new_folder)
                else:
                    return folder_selected

            else:
                retry_result = self.show_warning_message("Niste izabrali direktorijum. Pokušajte ponovo?")
                if retry_result == QMessageBox.StandardButton.No:
                    continue

    def create_new_folder(self, folder_selected, new_folder):
        new_folder_path = os.path.join(folder_selected, new_folder)
        try:
            os.makedirs(new_folder_path, exist_ok=True)
            print(f"Putanja novog foldera je: {new_folder_path}")
            return new_folder_path
        except Exception as e:
            self.show_critical_message(f"Greška pri kreiranju foldera: {e}")
            return None
        
        
""" 
# main.py
from backup_dialog import BackupDialog

if __name__ == "__main__":
    dialog = BackupDialog()
    selected_directory = dialog.choose_backup_directory()
    if selected_directory:
        print(f"Izabrani direktorijum ili kreirani folder: {selected_directory}")
    else:
        print("Nijedan direktorijum nije izabran.")
 """