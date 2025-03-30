import gettext
import os
from PySide6.QtWidgets import QLabel, QPushButton, QComboBox

from signal_manager import SignalManager

class TranslationManager:
    def __init__(self, app):
        self.app = app
        self.translations = {}
        self.signal_manager = SignalManager()
        self._signal()

    def _signal(self):
        self.signal_manager.connect_signal("signal_change_language", self, "load_translation")
        
    def add_widget(self, widget, text):
        # Koristi _() kao oznaku za prevođenje
        self.translations[widget] = _(text)
        self.refresh_widget(widget)

    def load_translation(self, lang_code):
        path = os.path.abspath(f'locale/{lang_code}/LC_MESSAGES/app.mo')
        print(f"Traži prevod na putanji: {path}")
        
        print(f"..... prevodiii.... {lang_code}")
        lang = gettext.translation('app', localedir='locale', languages=['cz'], fallback=True)
        lang.install()
        print(lang._info)  # Prikazuje informacije o učitanom prevodu

        global _
        _ = lang.gettext
        self.refresh_all()

    def refresh_all(self):
        for widget, text in self.translations.items():
            self.refresh_widget(widget)

    def refresh_widget(self, widget):
        # Ažurira widget sa prevedenim tekstom
        # Provjeri tip widget-a i ažuriraj tekst
        print(f"jednu po jednu.......... {_(self.translations[widget])}")
        if isinstance(widget, QLabel):
            widget.setText((_(self.translations[widget])))
        elif isinstance(widget, QPushButton):
            widget.setText((_(self.translations[widget])))
        elif isinstance(widget, QComboBox):
            for i in range(widget.count()):
                widget.setItemText(i, widget.itemText(i))