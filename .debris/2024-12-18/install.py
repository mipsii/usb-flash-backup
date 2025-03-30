from backup_dialog import BackupDialog
from config import ConfigManager

if __name__ == "__main__":
    config_manager = ConfigManager()
    dialog = BackupDialog()

    # Proveri postoji li već putanja za backup
    if not config_manager.get_backup_config():
        # Ako ne postoji, otvori dijalog za izbor direktorijuma
        backup_base_path = dialog.choose_backup_directory()
        if backup_base_path:
            config_manager.save_config("backup_base_path", backup_base_path)
            
            print(f"Putanja za backup je postavljena: {backup_base_path}")
        else:
            print("Nijedan direktorijum nije izabran za backup.")

    # Prikaz poruke nakon podešavanja
    dialog.show_info_message("Backup konfiguracija je uspešno postavljena.")
