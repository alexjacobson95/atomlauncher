import wx

class GUI(wx.Frame):
	def __init__(self, parent, id, title):
		wx.Frame.__init__(self, parent, id, title,  size=wx.Size(450, 200), style=wx.NO_BORDER)
		#self.SetBackgroundColour("blue")
		self.Centre();


app = wx.App(False)
frame = GUI(None, -1, "Atome Launcher")
frame.Show(True)
app.MainLoop()