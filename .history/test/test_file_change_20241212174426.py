import pytest
from file_change import FileChangeManager

@pytest.fixture
def file_change_manager():
    return FileChangeManager("/test/backup", "/test/usb")

def test_initialization(file_change_manager):
    assert file_change_manager.backup_path == "/test/backup"
    assert file_change_manager.usb_path == "/test/usb"
    assert file_change_manager.new_files == []

@pytest.mark.asyncio
async def test_clear_changes(file_change_manager):
    file_change_manager.new_files = ["/new_file.txt"]
    await file_change_manager.clear_changes()
    assert file_change_manager.new_files == []
