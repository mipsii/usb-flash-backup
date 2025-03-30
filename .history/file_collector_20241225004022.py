import asyncio
import json
import os
from PySide6.QtCore import Signal, QObject

from signal_manager import SignalManager

class FileCollector(QObject):
    send_merged_state = Signal(dict)

    def __init__(self):
        super().__init__()  # OBAVEZNO pozivanje QObject.__init__()
        self.current_backup_folder_path = None
        self._signals()

    def _signals(self):
        self.signal_manager = SignalManager()
     
    async def get_usb_files(self, usb_path):
        """
        Prikuplja sve fajlove sa datog USB uređaja.
        :param usb_path: Putanja do USB uređaja.
        :return: Rečnik sa relativnim putanjama kao ključevima i informacijama o fajlovima kao vrednostima.
        """
        usb_files = {
            os.path.relpath(os.path.join(root, file), usb_path): {
                'size': os.path.getsize(os.path.join(root, file)),
                'modification_time': os.path.getmtime(os.path.join(root, file))
            }
            for root, _, files_list in await asyncio.to_thread(lambda: list(os.walk(usb_path)))
            if not self.should_ignore(root)  # Ignorisanje neželjenih direktorijuma
            for file in files_list
            if not self.should_ignore(file)  # Ignorisanje neželjenih fajlova        
            }
        return usb_files
    
    def should_ignore(self, file_path):
        ignored_dirs = ['.Trash-1000', '.Trash', '.DS_Store']
        return any(ignored_dir in file_path for ignored_dir in ignored_dirs)

    def load_deleted_files(self, backup_path):
        """
        Učitaj listu izbrisanih fajlova iz `deleted_files.json`.
        """
        deleted_file_path = os.path.join(backup_path, "deleted_files.json")
        if os.path.exists(deleted_file_path):
            with open(deleted_file_path, "r") as f:
                return set(json.load(f))
        return set()

    def merge_backups(self, current_path, previous_state):
        """
        Kombinuj fajlove iz trenutnog backup-a sa prethodnim stanjem.
        :param current_path: Putanja trenutnog backup-a.
        :param previous_state: Stanje iz prethodnog backup-a (dict).
        :return: Kombinovano stanje fajlova.
        """
        deleted_files = self.load_deleted_files(current_path)
        current_files = {
            os.path.relpath(os.path.join(root, file), current_path): {
            'size': os.path.getsize(os.path.join(root, file)),
            'modification_time': os.path.getmtime(os.path.join(root, file))
            }
            for root, _, files_list in os.walk(current_path)
            for file in files_list
            if (file != "deleted_files.json") and (file != ".serial")  # Isključujemo specificirane fajlove
            }
        
        # Kombinovanje fajlova
        merged_state = previous_state.copy()
        for file, file_path in current_files.items():
            if file not in deleted_files:
                merged_state[file] = file_path  # Dodaj novi ili modifikovani fajl
        
        # Izuzimanje obrisanih fajlova
        for deleted_file in deleted_files:
            if deleted_file in merged_state:
                del merged_state[deleted_file]
        
        #(f"spojeni fajlovi su ....print..... { merged_state }")
        return merged_state

    async def recursive_backup_merge(self,current_backup_folder_path, history, target_index=None):
        """
        Rekurzivno kombinuje backup-ove do ciljanog indeksa `target_index`.
        :param history: Lista putanja svih backup-ova.
        :param current_index: Trenutni indeks u rekurziji.
        :param target_index: Ciljni indeks do kog se kombinuje (podrazumevano cela istorija).
        :param merged_state: Trenutno kombinovano stanje fajlova.
        :return: Kombinovano stanje fajlova.
        """
        print("----------------------------")
        self.current_backup_folder_path = current_backup_folder_path
        # Postavi ciljani indeks na kraj ako nije specificiran
        if target_index is None:
            target_index = len(history)
                    
        # Inicijalizacija kombinovanog stanja pri prvom pozivu
        merged_state = {}
        current_index = 0 
        return self.prosledjeni(history, current_index, target_index, merged_state)
        
    def prosledjeni(self, history, current_index, target_index, merged_state):
        
        if current_index > target_index or current_index >= len(history):
                # Ako smo stigli do ciljanog indeksa ili iza kraja istorije, prekidamo rekurziju
                self.send_merged_state.emit(merged_state)

                return merged_state 
            
        current_path = os.path.join(self.current_backup_folder_path, history[current_index])
        # Kombinuj trenutni backup sa prethodnim stanjem
        merged_state = self.merge_backups(current_path, merged_state)
        # Rekurzivno pozovi sledeći backup
        return self.prosledjeni(history, current_index + 1, target_index, merged_state)