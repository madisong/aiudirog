import wx
import wx.lib.agw.toasterbox as TB
from lib.Tools.Globals import *
from threading import Thread
from wx import GetClientDisplayRect as GCDR


class Notify(Thread):
    def __init__(self):
        Thread.__init__(self)
        
        self.start()
        
    def run(self):
        self.toaster = TB.ToasterBox(Globals.Frame, tbstyle=TB.TB_COMPLEX)
        self.toaster.SetPopupPauseTime(5000)

        tbpanel = self.toaster.GetToasterBoxWindow()
        panel = wx.Panel(tbpanel, -1, style=wx.BORDER_RAISED)
        sizer = wx.BoxSizer(wx.VERTICAL)

        button = wx.Button(panel, wx.ID_ANY, "Google Voice:\n\nNew Messages")
        button.Bind(wx.EVT_BUTTON,self.RequestUser)
        button.Bind(wx.EVT_BUTTON,self.Raise)
        sizer.Add(button, 0, wx.EXPAND)

        panel.SetSizer(sizer)
        panel.SetBackgroundColour("#AFEEEE")
        self.toaster.AddPanel(panel)

        wx.CallAfter(self.toaster.Play)
    
    def RequestUser(self, event=None):
        Globals.Frame.RequestUserAttention(1)
    
    def Raise(self, event=None):
        Globals.Frame.Raise()
