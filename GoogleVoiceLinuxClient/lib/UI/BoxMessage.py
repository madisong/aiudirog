import wx
from lib.UI.MsgPopUp import *

class BoxMessage(wx.Panel):
    def __init__(self, parent, convo, *args, **kws):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY,style=wx.BORDER_SUNKEN)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        NAME = convo[0]['from']
        MSG = convo[-1]['text']
        self.CONVO = convo
        
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
        
        self.SetSizer(hbox)
        self.Fit()

    def ChangeName(self,NAME):
        self.name.SetLabel(NAME)
    
    def ChangeMsg(self,MSG):
        self.name.SetLabel(MSG)

    def PopUp(self, instance):
        self.POP = MsgPopUp(self, self.CONVO)
        self.POP.Show()
