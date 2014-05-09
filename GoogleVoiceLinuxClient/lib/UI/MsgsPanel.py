import  wx
import  wx.lib.scrolledpanel as scrolled
from lib.UI.BoxMessage import *

class MsgsPanel(scrolled.ScrolledPanel):
    def __init__(self, parent):
        scrolled.ScrolledPanel.__init__(self, parent, -1)
        self.MSGBox = wx.BoxSizer(wx.VERTICAL)
        self.CurrentBox = []
        self.SetSizer(self.MSGBox)
        self.SetAutoLayout(1)
        self.SetupScrolling()

    def AddMessage(self, NAME, MSG):
        MSG = BoxMessage(self,NAME,MSG)
        self.CurrentBox.append(MSG)
        self.MSGBox.Add(MSG,0,wx.EXPAND|wx.ALL,5)
