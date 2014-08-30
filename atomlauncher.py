#win32con comes from: http://sourceforge.net/projects/pywin32/files/pywin32/

import wx
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


class Window(wx.Frame):
	def __init__(self, parent, id, title):
		wx.Frame.__init__(self, parent, id, title, size=wx.Size(450, 200), style=wx.NO_BORDER)
		self.SetBackgroundColour("red")
		self.Centre()

		#Hotkey Setup
		self.regHotKey()
		self.Bind(wx.EVT_HOTKEY, self.handleAltEnter, id=self.hotKeyIDs[0])
		self.Bind(wx.EVT_HOTKEY, self.handleAltQ, id=self.hotKeyIDs[1])

		#main textbox
		self.control = wx.TextCtrl(self, -1, 'enter a command', size=wx.Size(200, 20), style=wx.TE_PROCESS_TAB)
		self.control.Centre()

	def regHotKey(self):
		self.hotKeyIDs = [ 100, 101 ]
		self.RegisterHotKey(self.hotKeyIDs[0], win32con.MOD_ALT, win32con.VK_RETURN)
		self.RegisterHotKey(self.hotKeyIDs[1], win32con.MOD_ALT, 81) #81 should be q...I think?

	def handleAltEnter(self, event):
		toggleWindow()

		#if mainWindow.IsShown():

	def handleAltQ(self, event):
		quit()

			


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