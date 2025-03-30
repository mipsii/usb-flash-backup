

import pyudev


class USBManagerWindows:
    def mount_usb(self, device):
        # Implementacija za montiranje USB-a na Windowsu
        self.device = device

    def get_usb_serial_windows(self):
        """Hvatanje serijskog broja USB uređaja na Windows-u."""
        import wmi
        c = wmi.WMI()
        usb_devices = []
        for usb in c.Win32_DiskDrive():
            if "USB" in usb.Caption:
                usb_devices.append(usb)
        return usb_devices

    def get_connected_usb_devices_windows(self):
        """Vraća listu povezanih USB uređaja sa njihovim serijskim brojevima i montiranim putanjama."""
        c = wmi.WMI()
        usb_devices = []
        
        # Prvo dohvatamo sve USB uređaje sa serijskim brojem i DeviceID
        usb_list = [(usb.SerialNumber, usb.DeviceID) for usb in c.Win32_DiskDrive() if "USB" in usb.Caption]
        
        # Dohvatamo sve logičke drajvove
        logical_drives = win32api.GetLogicalDriveStrings().split('\000')[:-1]

        # Prolazimo kroz svaki logički drajv koji je prijavljen kao USB uređaj
        wmi_service = win32com.client.Dispatch("WbemScripting.SWbemLocator").ConnectServer(".", "root\\cimv2")
        for drive in logical_drives:
            if win32api.GetDriveType(drive) == win32api.DRIVE_REMOVABLE:
                # Pretražujemo particije i povezane logičke diskove
                for serial, device_id in usb_list:
                    for partition in wmi_service.ExecQuery(f"ASSOCIATORS OF {{Win32_DiskDrive.DeviceID='{device_id}'}} WHERE AssocClass=Win32_DiskDriveToDiskPartition"):
                        for logical_disk in wmi_service.ExecQuery(f"ASSOCIATORS OF {{Win32_DiskPartition.DeviceID='{partition.DeviceID}'}} WHERE AssocClass=Win32_LogicalDiskToPartition"):
                            if logical_disk.DeviceID == drive:
                                # Dodajemo USB uređaj sa serijskim brojem i montiranom putanjom
                                usb_devices.append({
                                    'serial_number': serial,
                                    'mount_point': drive,
                                    'label': logical_disk.VolumeName
                                })
        return usb_devices
    def get_usb_info_windows(self, device_path):
        """
        Koristi pyudev ili WinAPI za detekciju USB uređaja na Windowsu.
        """
        # Primer: Koristite pyudev za Windows
        context = pyudev.Context()
        for device in context.list_devices(subsystem='usb', DEVTYPE='usb_device'):
            if device.get('ID_SERIAL') and device.get('DEVNAME') == device_path:
                serial_number = device.get('ID_SERIAL')
                label = device.get('ID_FS_LABEL')
                mount_point = device.get('DEVNAME')  # Proveriti kako WinAPI daje mount_point
                return device_path, mount_point, serial_number, label
        return None
