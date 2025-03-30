POT_FILE = messages.pot
PO_DIR = locale
PO_FILES = $(PO_DIR)/sr/LC_MESSAGES/app.po $(PO_DIR)/cs/LC_MESSAGES/app.po $(PO_DIR)/en/LC_MESSAGES/app.po
MO_FILES = $(PO_DIR)/sr/LC_MESSAGES/app.mo $(PO_DIR)/cs/LC_MESSAGES/app.mo $(PO_DIR)/en/LC_MESSAGES/app.mo

all: $(MO_FILES)

$(POT_FILE):
	find . -name '*.py' -not -path './.history/*' -not -path './.debris/*' | xargs xgettext --keyword=_ --from-code=UTF-8 -o $(POT_FILE)

$(PO_DIR)/%/LC_MESSAGES/app.po: $(POT_FILE)
	mkdir -p $(@D) # Create the directory if it doesn't exist
	cp $(POT_FILE) $@

$(PO_DIR)/%/LC_MESSAGES/app.mo: $(PO_DIR)/%/LC_MESSAGES/app.po
	mkdir -p $(@D) # Ensure the target directory exists for .mo files
	echo "Compiling $< to $@" # Debug line to see what is being compiled
	echo "-------------------------------"
	msgfmt $< -o $@

clean:
	rm -f $(POT_FILE)
	rm -f $(PO_DIR)/*/LC_MESSAGES/app.po
	rm -f $(PO_DIR)/*/LC_MESSAGES/app.mo
