import wx
from lib.UI.MainFrame import *



app = wx.App(False)
name = "Google Voice Linux"
frame = MainFrame(None, name)
app.MainLoop()
