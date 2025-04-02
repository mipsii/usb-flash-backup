import gettext

lang = gettext.translation('app', localedir='locale', languages=['sr'])
lang.install()
_ = lang.gettext  # Postavljamo globalni alias
