import wx
from lib.Tools.Globals import *
from wx.lib.pubsub import setupv1
from wx.lib.pubsub import Publisher as pub
from lib.Tools.TextCtrlAutoComplete import TextCtrlAutoComplete

class ComposeWindow(wx.Dialog):
    """
    Pop-up for composition of a new message.
    """
    
    def __init__(self, parent=None, *args, **kw):
        wx.Dialog.__init__(self, parent=None, id=wx.ID_ANY, size=(450,300))
        self.SetWindowStyle(self.GetWindowStyle()|wx.RESIZE_BORDER)
        
        Panel = wx.Panel(self)
        
        TOtxt = wx.StaticText(Panel, -1, "To:")
        #self.TO = wx.TextCtrl(Panel)
        self.TO = TextCtrlAutoComplete(Panel, choices=Globals.ContactNames)
        MSGtxt = wx.StaticText(Panel, -1, "Message:")
        self.MSG = wx.TextCtrl(Panel,style=wx.TE_MULTILINE)
        send = wx.Button(Panel, -1, "Send")
        send.Bind(wx.EVT_BUTTON, self.Send)
        
        VBOX = wx.BoxSizer(wx.VERTICAL)
        VBOX.Add(TOtxt,0,wx.EXPAND|wx.ALL,5)
        VBOX.Add(self.TO,0,wx.EXPAND|wx.ALL,5)
        VBOX.Add(MSGtxt,0,wx.EXPAND|wx.ALL,5)
        VBOX.Add(self.MSG,1,wx.EXPAND|wx.ALL,5)
        VBOX.Add(send,0,wx.ALIGN_RIGHT|wx.ALL,5)
        
        Panel.SetSizer(VBOX)
        Panel.Layout()
        
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
        self.Layout()
        self.ShowModal()
    
    def Send(self, event=None):
        text = self.MSG.GetValue()
        to = self.TO.GetValue()
        if text == "" or text.replace("\n","") == "":
            return
        if to in Globals.ContactNames:
            to = Globals.Contacts[to]
        Globals.Voice.send_sms(to, text)
        wx.CallAfter(pub.sendMessage,"ThreadForReLoadFolder",data=None)
        self.OnClose()
    
    def OnClose(self, event=None):
        self.Destroy()