#win32con comes from: http://sourceforge.net/projects/pywin32/files/pywin32/

import wx
import wx.stc as stc
import win32con

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

class CommandBox(stc.StyledTextCtrl):
	def __init__(self, parent, style):
		stc.StyledTextCtrl.__init__(self, parent, style=style)


class Window(wx.Frame):
	def __init__(self, parent, id, title):
		wx.Frame.__init__(self, parent, id, title, size=(450, 200), style=wx.NO_BORDER)

		#Hotkey Setup
		self.hotKeyIDs = [ 100, 101 ]
		self.regHotKey()
		self.Bind(wx.EVT_HOTKEY, self.handleAltEnter, id=self.hotKeyIDs[0])
		self.Bind(wx.EVT_HOTKEY, self.handleAltQ, id=self.hotKeyIDs[1])

		#sizers
		self.hbox = wx.BoxSizer(wx.HORIZONTAL)
		self.panel1 = wx.Panel(self, -1, style=wx.BORDER_NONE)
		self.panel2 = wx.Panel(self, -1, style=wx.BORDER_NONE)
		self.panel3 = wx.Panel(self, -1, style=wx.BORDER_NONE)

		self.hbox.Add(self.panel1, -1, wx.EXPAND)
		self.hbox.Add(self.panel2, -1, wx.EXPAND)
		self.hbox.Add(self.panel3, -1, wx.EXPAND)

		self.titleText = wx.StaticText(self.panel1, 0, 'Atom Launcher', size=(100,50), style=wx.ALIGN_CENTRE)

		self.commandBox = wx.TextCtrl(self.panel2, 1, '', size=(200, 20), style=wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB)
	
		self.textBox = wx.TextCtrl(self.panel3, 2, 'Test', size=(200, 40))

		self.SetSizer(self.hbox)


		self.SetBackgroundColour("white")
		self.Centre()
		#CommandBox(self, wx.SIMPLE_BORDER)


		#self.control.Bind(wx.EVT_TEXT_ENTER, self.handleEnter)

	def regHotKey(self):
		self.RegisterHotKey(self.hotKeyIDs[0], win32con.MOD_ALT, win32con.VK_RETURN)
		self.RegisterHotKey(self.hotKeyIDs[1], win32con.MOD_ALT, 81) #81 should be q...I think?

	def handleAltEnter(self, event):
		toggleWindow()

		#if mainWindow.IsShown():

	def handleAltQ(self, event):
		quit()

	def handleEnter(self, event):
		self.commandBox.GetText()

			


class TaskBarIcon(wx.TaskBarIcon):
	def __init__(self):
		super(TaskBarIcon, self).__init__()
		self.set_icon(TRAY_ICON)
		self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

		toggleWindow()

	def CreatePopupMenu(self):
		menu = wx.Menu()
		create_menu_item(menu, 'Say Hello', self.on_hello)
		menu.AppendSeparator()
		create_menu_item(menu, 'Exit', self.on_exit)
		return menu

	def set_icon(self, path):
		icon = wx.IconFromBitmap(wx.Bitmap(path))
		self.SetIcon(icon, TRAY_TOOLTIP)

	def on_left_down(self, event):
		toggleWindow()

	def on_hello(self, event):
		toggleWindow()

	def on_exit(self, event):
		quit()

app = wx.App(False)
mainWindow = Window(None, -1, "Atom Launcher")
icon = TaskBarIcon()
app.MainLoop()