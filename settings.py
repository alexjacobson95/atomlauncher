import os

SETTINGS_FILE = 'settings.txt'
DEFAULT_SETTINGS = """\
launchShortCut: alt-enter
quitShortCut: alt-Q
"""

def readSettingsFile():
	if os.path.isfile(SETTINGS_FILE):
		with open(SETTINGS_FILE, 'r') as settingsFile:
			for line in settingsFile:
				print line

	else:
		with open(SETTINGS_FILE, 'w') as settingsFile:
			settingsFile.write(DEFAULT_SETTINGS)

		return readSettingsFile()


readSettingsFile()