import wx
from lib.UI.MsgPopUp import *
from wx.lib.pubsub import setupv1
from wx.lib.pubsub import Publisher as pub
from lib.Tools.BaseColorChangeObj import *


class BoxMessage(wx.Panel,BaseColorChangeObj):
    def __init__(self, parent, convo, *args, **kws):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY,style=wx.BORDER_SUNKEN)
        BaseColorChangeObj.__init__(self,"BoxMessage")
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        for c in convo:
            NAME = c['from']
            if NAME != "Me:": break
        
        MSG = convo[-1]['text'].replace("\n","")
        if len(MSG) > 35:
            MSG = MSG[:35]+"..."
        self.ID = str(convo[0]['id'])
        
        self.CONVO = convo
        wx.CallAfter(pub.sendMessage,self.ID,data=self.CONVO)
        
        self.name = wx.StaticText(self, -1, NAME)
        self.msg = wx.StaticText(self, -1, MSG)
        NameFont = wx.Font(12, wx.DECORATIVE, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD)
        self.name.SetFont(NameFont)

        vbox.Add(self.name, 0, wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, 5)
        vbox.Add(self.msg, 0, wx.EXPAND|wx.BOTTOM|wx.LEFT|wx.RIGHT, 5)
        hbox.Add(vbox, 0, wx.EXPAND|wx.ALL, 0)
        
        self.Bind(wx.EVT_LEFT_UP, self.PopUp)
        self.name.Bind(wx.EVT_LEFT_UP, self.PopUp)
        self.msg.Bind(wx.EVT_LEFT_UP, self.PopUp)
        
        self.SetBackgroundColour("#FFFFFF")
        
        self.SetSizer(hbox)
        self.Fit()

    def ChangeName(self,NAME):
        self.name.SetLabel(NAME)
    
    
    def ChangeMsg(self,MSG):
        self.name.SetLabel(MSG)

    def PopUp(self, instance):
        if self.ID not in Globals.OpenConvos:
            self.POP = MsgPopUp(self, self.CONVO,self.ID)
            self.POP.Show()
        else:
            wx.CallAfter(pub.sendMessage,"RAISE"+self.ID,data=None)