import os

SETTINGS_FILE = 'settings.txt'
DEFAULT_SETTINGS = """\
launchShortCut alt-enter
quitShortCut alt-Q
"""

settingsDict = {}

def readSettingsFile():
	if not os.path.isfile(SETTINGS_FILE):
		with open(SETTINGS_FILE, 'w') as settingsFile:
			settingsFile.write(DEFAULT_SETTINGS)

		readSettingsFile()

	else:
		with open(SETTINGS_FILE, 'r') as settingsFile:
			for line in settingsFile:
				typeBuffer = ''
				setBuffer = ''
				setSetting = False

				for c in line:
					if c == '\n':
						settingsDict[typeBuffer] = setBuffer
						typeBuffer = ''
						setBuffer = ''
						setSetting = False

					else:
						if  c == ' ':
							setSetting = True
						else:
							if not setSetting:
								typeBuffer += c
							else:
								setBuffer += c

readSettingsFile()
print settingsDict