import wx
import sys
from lib.UI.MsgsPanel import *
from wx import GetClientDisplayRect as GCDR
from lib.Tools.Globals import *
from PreferenceEditor import PreferenceEditor

class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        #Align window to bottom-right
        dw, dh = wx.GetDisplaySize()
        x = dw - 300
        wx.Frame.__init__(self, parent, title=title, 
                          size=(300,GCDR()[3]-2*GCDR()[1]),
                          pos=(x,GCDR()[1]))
        Panel = MsgsPanel(self)
        
        optmenu = wx.Menu()
        PrefID = wx.NewId()
        optmenu.Append(PrefID, "&Preferences"," ")
        self.Bind(wx.EVT_MENU, self.Options, id=PrefID)
        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(optmenu,"&Options")
        self.SetMenuBar(menuBar)
        
        Globals.Frame = self
        
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Show()
        self.Layout()
        
    def Options(self, event=None):
        PreferenceEditor()

    def OnClose(self, event):
        self.Destroy()
        sys.exit()

