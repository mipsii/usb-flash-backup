import gettext

class TranslationManager:
    def __init__(self, app):
        self.app = app
        self.translations = {}

    def add_widget(self, widget, text):
        # Koristi _() kao oznaku za prevođenje
        self.translations[widget] = _(text)
        self.refresh_widget(widget)

    def load_translation(self, lang_code):
        lang = gettext.translation('app', localedir='locale', languages=[lang_code], fallback=True)
        lang.install()
        global _
        _ = lang.gettext
        self.refresh_all()

    def refresh_all(self):
        for widget, text in self.translations.items():
            self.refresh_widget(widget)

    def refresh_widget(self, widget):
        # Ažurira widget sa prevedenim tekstom
        widget.setText(self.translations[widget])
