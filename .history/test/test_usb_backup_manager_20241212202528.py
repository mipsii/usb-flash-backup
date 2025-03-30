import os
import pytest
from file_change import FileChangeManager
from usb_backup_manager import USBBackupManager

@pytest.fixture
def setup_test_dirs(tmp_path):
    usb_path = tmp_path / "test_usb"
    backup_path = tmp_path / "test_backup"
    usb_path.mkdir()
    backup_path.mkdir()
    with open(usb_path / "new_file.txt", "w") as f:
        f.write("Novi sadržaj")
    return str(usb_path), str(backup_path)

@pytest.mark.asyncio
def test_sync_creates_new_file(setup_test_dirs):
    usb_path, backup_path = setup_test_dirs
    file_change_manager = FileChangeManager()
    manager = USBBackupManager(file_change_manager)  # Ispravno pozivanje konstruktora
    
    # Poziv metode sync
    await manager.sync(usb_path, backup_path)
