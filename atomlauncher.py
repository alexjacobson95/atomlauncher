import wx

TRAY_TOOLTIP = 'System Tray Demo'
TRAY_ICON = 'atom.png'

def create_menu_item(menu, label, func):
	item = wx.MenuItem(menu, -1, label)
	menu.Bind(wx.EVT_MENU, func, id=item.GetId())
	menu.AppendItem(item)
	return item


class Window(wx.Frame):
	def __init__(self, parent, id, title):
		wx.Frame.__init__(self, parent, id, title, size=wx.Size(450, 200), style=wx.NO_BORDER)
		self.SetBackgroundColour("red")
		self.Centre()

class TaskBarIcon(wx.TaskBarIcon):
	def __init__(self):
		super(TaskBarIcon, self).__init__()
		self.set_icon(TRAY_ICON)
		self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

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
		print 'Tray icon was left-clicked'

	def on_hello(self, event):
		mainWindow.Show(True)

	def on_exit(self, event):
		mainWindow.Destroy()
		wx.CallAfter(self.Destroy)

app = wx.App(False)
mainWindow = Window(None, -1, "Atom Launcher")
TaskBarIcon()
app.MainLoop()


#class GUI(wx.Frame):
#	def __init__(self, parent, id, title):
#		wx.Frame.__init__(self, parent, id, title,  size=wx.Size(450, 200), style=wx.NO_BORDER)
#		self.SetBackgroundColour("orange")
#		self.Centre()


#app = wx.Ap(False)
#frame = GUI(None, -1, "Atom Launcher")
#frame.Show(True)
#app.MainLoop()