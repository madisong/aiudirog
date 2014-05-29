import wx
from lib.UI.MainFrame import *
import os
import ConfigParser

Globals.INI = ConfigParser.ConfigParser()
Globals.ini_path = os.path.join("Color.ini")
Globals.INI.read(Globals.ini_path)

app = wx.App(False)
name = "Google Voice Linux"
frame = MainFrame(None, name)
app.MainLoop()
