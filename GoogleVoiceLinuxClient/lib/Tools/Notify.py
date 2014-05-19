import wx
import wx.lib.agw.toasterbox as TB
from lib.Tools.Globals import *
from threading import Thread

class Notify(Thread):
    def __init__(self):
        Thread.__init__(self)
        
        self.start()
        
    def run(self):
        self.toaster = TB.ToasterBox(Globals.Frame, tbstyle=TB.TB_SIMPLE)
        self.toaster.SetPopupPauseTime(3000)
        self.toaster.SetPopupText("Google Voice: New Messages")
        wx.CallAfter(self.toaster.Play)
