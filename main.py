#!/usr/bin/env python

import wx
from lib.UI.MainFrame import *
import os
import ConfigParser

#Prepare the color ini for use by other classes
Globals.INI = ConfigParser.ConfigParser()
Globals.path = os.path.dirname(__file__)
Globals.ini_path = os.path.join(Globals.path,'resources',"Color.ini")
Globals.INI.read(Globals.ini_path)

#Start the app
app = wx.App(False)
name = "Google Voice Linux"
frame = MainFrame(None, name)
app.MainLoop()
