import wx
from lib.Tools.Globals import *
from lib.Tools.BaseColorChangeObj import *
import json
from lib.Tools.ExtraFunctions import *



class ConvoMsg(wx.Panel,BaseColorChangeObj):
    def __init__(self, parent, msg, *args, **kws):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY,style=wx.BORDER_SUNKEN)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        NAME = msg['from']
        MSG = msg['text']
        TIME = msg['time']
        
        self.name = wx.StaticText(self, -1, NAME)
        self.msg = wx.StaticText(self, -1, MSG)
        NameFont = wx.Font(10, wx.DECORATIVE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.name.SetFont(NameFont)
        self.time = wx.StaticText(self, -1, TIME)
        TimeFont = wx.Font(7, wx.DECORATIVE, wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL)
        self.time.SetFont(TimeFont)

        vbox.Add(self.name, 0, wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, 5)
        vbox.Add(self.msg, 0, wx.EXPAND|wx.BOTTOM|wx.LEFT|wx.RIGHT, 5)
        vbox.Add(self.time, 0, wx.EXPAND|wx.BOTTOM|wx.LEFT|wx.RIGHT, 5)
        hbox.Add(vbox, 0, wx.EXPAND|wx.ALL, 0)
        
        if NAME != "Me:":
            color = "#AFEEEE"
            self.Name = "ConvoMsgYOU"
        else:
            color = "#FFFFFF"
            self.Name = "ConvoMsgME"
        try: 
            self.SetBackgroundColour(GetTupleFromString(
                                             Globals.INI.get("MAIN",self.Name)))
        except: 
            self.SetBackgroundColour(color)
        try: 
            color = GetTupleFromString(Globals.INI.get("MAIN",self.Name+"TEXT"))
            self.name.SetForegroundColour(color)
            self.msg.SetForegroundColour(color)
            self.time.SetForegroundColour(color)
        except: 
            pass
        BaseColorChangeObj.__init__(self,self.Name)
        self.SetSizer(hbox)
        self.Fit()

    def ChangeName(self,NAME):
        self.name.SetLabel(NAME)
    
    def ChangeMsg(self,MSG):
        self.name.SetLabel(MSG)
