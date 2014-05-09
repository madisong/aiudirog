import wx
import sys
from lib.UI.MsgsPanel import *
from wx import GetClientDisplayRect as GCDR

class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        #Align window to bottom-right
        dw, dh = wx.GetDisplaySize()
        x = dw - 300
        wx.Frame.__init__(self, parent, title=title, 
                          size=(300,GCDR()[3]-2*GCDR()[1]),
                          pos=(x,GCDR()[1]))
        Panel = MsgsPanel(self)
        
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Show()
        self.Layout()

    def OnClose(self, instance):
        sys.exit()

