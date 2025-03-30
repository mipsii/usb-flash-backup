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
async def test_sync(setup_test_dirs):
    # Dobijanje testnih direktorijuma
    usb_path, backup_path = setup_test_dirs

    # Inicijalizacija FileChangeManager sa potrebnim argumentima
    file_change_manager = FileChangeManager(backup_path=backup_path, usb_path=usb_path)

    # Inicijalizacija USBBackupManager
    manager = USBBackupManager(file_change_manager)

    # Poziv asinhrone metode sync
    await manager.sync(usb_path, backup_path)

    # Provere rezultata (dodaj prema potrebama)
    # Na primer, proveri da li su datoteke sinhronizovane kako treba