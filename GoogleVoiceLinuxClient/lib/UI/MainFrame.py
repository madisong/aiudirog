import wx
from lib.UI.MsgsPanel import *

class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, 
                          size=(300,wx.GetDisplaySize()[1]))
        Panel = MsgsPanel(self)
        
        self.Show()


