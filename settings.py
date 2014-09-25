import os

SETTINGS_FILE = 'settings.txt'
DEFAULT_SETTINGS = """\
trayToolTip AtomLauncher
trayIcon atom.png
launchHotKey alt-enter
quitHotKey alt-Q
"""

def readSettingsFile():
	settings = {}

	if not os.path.isfile(SETTINGS_FILE):
		with open(SETTINGS_FILE, 'w') as settingsFile:
			settingsFile.write(DEFAULT_SETTINGS)

		print 'Settings File Created'
		readSettingsFile()

	else:
		with open(SETTINGS_FILE, 'r') as settingsFile:
			for line in settingsFile:
				typeBuffer = ''
				setBuffer = ''
				setSetting = False

				for c in line:
					if not(typeBuffer == '' and c == '\n'):
						if c == '\n':
							settings[typeBuffer] = setBuffer
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

	return settings

def checkSettingsFile():
	print 'test'

#readSettingsFile()
#print settings