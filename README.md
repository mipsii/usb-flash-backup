
# USB Flash Backup Program

This program allows users to create backups of data on USB devices using GIT versioning. The application enables users to back up files and track changes on USB devices.

## Features

- **Automated backup**: Create backup copies of data from USB devices to a local disk.
- **GIT versioning support**: All file changes are tracked using GIT, making it easy to follow history and revert to previous versions.
- **User interface**: The application uses **PyQt/PySide** for the graphical user interface (GUI), providing a simple way to use the application on desktop computers.

## Installation

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/mipsii/usb-flash-backup.git
   ```

2. Run the `install.py` script to install dependencies:
   ```bash
   python install.py
   ```

3. After the installation is complete, run the application:
   ```bash
   python main.py
   ```

## Starting the Application

In the `main.py` file, the application initializes and checks for an existing backup configuration. If no backup path is set, it prompts the user to choose a backup directory. Here’s how it starts:

```python
from backup_dialog import BackupDialog
from config import ConfigManager

if __name__ == "__main__":
    config_manager = ConfigManager()
    dialog = BackupDialog()

    # Check if a backup path is already set
    if not config_manager.get_backup_config():
        # If not, open the dialog to choose a directory
        backup_base_path = dialog.choose_backup_directory()
        if backup_base_path:
            config_manager.save_config("backup_base_path", backup_base_path)
            
            print(f"Backup path has been set: {backup_base_path}")
        else:
            print("No directory was selected for backup.")

    # Show a message after configuration
    dialog.show_info_message("Backup configuration has been successfully set.")
```

- `ConfigManager` handles the backup configuration (checking and saving paths).
- `BackupDialog` presents a dialog box for the user to choose a backup directory.
- If no backup path exists, the program will prompt the user to select one.

## Issues

- **Compatibility with PySide6 and newer Python versions**: The application worked well until January 2025, but with newer versions of Python and PySide6, errors occur when starting the application. The issue is due to incompatibilities between PySide6 and certain functions used in the code, which might require fixes or updates to the library versions.

- **Current error**: In the latest Python version with PySide6, the application fails to run due to errors related to compatibility between PySide6 and some methods used in the application.

## Contributing

If you'd like to contribute to this project, feel free to fork the repository and submit a pull request with your changes. Your contributions are welcome!
