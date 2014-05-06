import wx
import sys
from lib.UI.MainFrame import *

def OnClose(instance):
    sys.exit()
    
app = wx.App(False)
name = "Google Voice Linux"
frame = MainFrame(None, name)
frame.Bind(wx.EVT_CLOSE, OnClose)

app.MainLoop()