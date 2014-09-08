#win32con comes from: http://sourceforge.net/projects/pywin32/files/pywin32/

import wx
import wx.html
import win32con
import settings as s
import indexer

TRAY_TOOLTIP = 'Atom Launcher'
TRAY_ICON = 'atom.png'

def create_menu_item(menu, label, func):
	item = wx.MenuItem(menu, -1, label)
	menu.Bind(wx.EVT_MENU, func, id=item.GetId())
	menu.AppendItem(item)
	return item

def toggleWindow():
		mainWindow.Show(not mainWindow.IsShown())

def quit():
	mainWindow.Destroy()
	icon.Destroy()

class suggestionBox(wx.html.HtmlWindow):
	def __init__(self, parent, size, pos, style=None):
		self.html = wx.html.HtmlWindow(parent, 2, pos=pos, size=size, style=style)
		self.html.SetRelatedFrame(parent, "HTML : %%s")

		self.html.SetBorders(0)

		self.suggestions = []
		self.htmlCode = ''
		self.defaultCommands = [ 
			{'value': 'Google:', 'type': 'Google Search', 'search': ''},
			{'value': 'Run:',    'type': 'Run',           'run': ''},
			{'value': 'Find:',   'type': 'Find',          'find': ''}
		]
		#self.suggestion = {'value': 'Google:', 'type': 'Google Search', 'search': ''}


	def addSuggestion(self, suggestion):
		self.suggestions.append(suggestion)
		self.updateHtml()

	def clearSuggestions(self):
		self.suggestions = []
		self.updateHtml()

	def defaultSuggestions(self):
		self.clearSuggestions()
		self.suggestions.extend(self.defaultCommands)
		self.updateHtml()

	def updateHtml(self):
		self.htmlCode = '<ul>'
		for item in self.suggestions:
			self.htmlCode += '<li>' + item['value'] + '</li>'

		self.htmlCode += '</ul>'

		self.html.SetPage(self.htmlCode)

class TaskBarIcon(wx.TaskBarIcon):
	def __init__(self):
		super(TaskBarIcon, self).__init__()
		
		icon = wx.IconFromBitmap(wx.Bitmap(s.settings['trayicon']))
		self.SetIcon(icon, s.settings['trayToolTip'])
		
		self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.onLeftDown)

		toggleWindow()

	def CreatePopupMenu(self):
		menu = wx.Menu()
		create_menu_item(menu, 'Say Hello', self.onHello)
		menu.AppendSeparator()
		create_menu_item(menu, 'Exit', self.onExit)
		return menu

	def onLeftDown(self, event):
		toggleWindow()

	def onHello(self, event):
		toggleWindow()

	def onExit(self, event):
		quit()

class Window(wx.Frame):
	def __init__(self, parent, id, title):
		wx.Frame.__init__(self, parent, id, title, size=(450, 200), style=wx.NO_BORDER)

		#load settings
		s.readSettingsFile()

		#Hotkey Setup
		self.registerHotKeys()

		#bind window change
		self.Bind(wx.EVT_ACTIVATE, self.handleLostFocus, id=200)

		#window contents
		self.titleText = wx.StaticText(self, 0, 'Atom Launcher', style=wx.ALIGN_CENTRE)
		self.titleFont = wx.Font(24, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
		self.titleText.SetFont(self.titleFont)

		self.commandBox = wx.TextCtrl(self, 1, '', size=(450, 20), style=wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB)

		self.suggestionBox = suggestionBox(self, pos=(0, 60), size=(450, 140), style=wx.html.HW_SCROLLBAR_NEVER)
		
		#bind textevents
		self.commandBox.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
		self.commandBox.Bind(wx.EVT_KEY_UP, self.onKeyUp)

		#sizers1
		self.vbox = wx.BoxSizer(wx.VERTICAL)

		self.vbox.Add(self.titleText, flag=wx.ALIGN_CENTER)
		self.vbox.Add(self.commandBox, flag=wx.ALIGN_CENTER)

		self.SetSizer(self.vbox)
		self.Layout()

		self.Center()

	def registerHotKeys(self):
		launchHotKey = self.convertHotKeySettings(s.settings['launchHotKey'])
		quitHotkey = self.convertHotKeySettings(s.settings['quitHotkey'])

		self.hotKeyIDs = [ 100, 101 ]
		self.RegisterHotKey(self.hotKeyIDs[0], win32con.MOD_ALT, win32con.VK_RETURN)
		self.RegisterHotKey(self.hotKeyIDs[1], win32con.MOD_ALT, 81) #81 should be q...I think?

		self.Bind(wx.EVT_HOTKEY, self.handleAltEnter, id=self.hotKeyIDs[0])
		self.Bind(wx.EVT_HOTKEY, self.handleAltQ, id=self.hotKeyIDs[1])

	def convertHotKeySettings(self, setting):
		hotkey = setting.split('-')

		if hotkey[0] == 'ctrl':
			hotkey[0] = win32con.MOD_CTRL

		elif hotkey[0] == 'alt':
			hotkey[0] = win32con.MOD_ALT

		elif hotkey[0] == 'shift':
			hotkey[0] = win32con.MOD_SHIFT

		else:
			print 'ERROR: Couldn\'t set hotkey ' + setting
			return None

		if hotkey[1] == 'enter':
			hotkey[1] = win32con.VK_RETURN
		elif isalpha(hotkey[1]) or isdigit(hotkey[1]):
			


		return hotkey

	def handleAltEnter(self, event):
		toggleWindow()

		#if mainWindow.IsShown():

	def handleAltQ(self, event):
		quit()

	def handleLostFocus(self, event):
		print 'handled'

	def onKeyDown(self, event):
		code = event.GetKeyCode()

		if code == wx.WXK_UP:
			print("Up")
		elif code == wx.WXK_DOWN:
			print("Down")
		elif code == wx.WXK_RIGHT:
			print("Right")
		elif code == wx.WXK_LEFT:
			print("Left")

		event.Skip()

	def onKeyUp(self, event):
		code = event.GetKeyCode()
		
		if code == wx.WXK_RETURN:
			print("Return")

		#elif code == wx.WXK_BACK:     
		#	print("Backspace")

		#elif code == wx.WXK_DELETE:
		#	print("Delete")

		else:
			val = self.commandBox.GetValue()
			print val

			if val == '' or val == ' ':
				self.suggestionBox.defaultSuggestions()
			else:
				self.suggestionBox.clearSuggestions()
		
		event.Skip()

app = wx.App(False)
mainWindow = Window(None, -1, "Atom Launcher")
icon = TaskBarIcon()
app.MainLoop()


