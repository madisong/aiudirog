import wx
from lib.Tools.Globals import *
from lib.UI.ConvoMsg import *
import  wx.lib.scrolledpanel as scrolled
from wx.lib.pubsub import setupv1
from wx.lib.pubsub import Publisher as pub

class MsgPopUp(wx.Frame):
    def __init__(self, parent=None, CONVO=None, ID=None, *args, **kw):
        wx.Frame.__init__(self, parent=None, id=wx.ID_ANY, size=(450,500))
        
        for c in CONVO:
            NAME = c['from']
            if NAME != "Me:": break
        self.SetTitle(NAME.rstrip(":"))
        
        self.ConvoPanel = MainConvoPanel(self,CONVO,ID)
        
        self.Layout()
        
        
    def LoadConvo(self,event=None):
        self.ConvoPanel.LoadConversation()
        self.Layout()
        
    
class MainConvoPanel(wx.Panel):
    def __init__(self, parent, CONVO, ID, *args, **kws):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY,style=wx.BORDER_SUNKEN)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        
        self.Conversation = Conversation(self,CONVO, ID)
        
        vbox.Add(self.Conversation,5,wx.EXPAND|wx.LEFT|wx.RIGHT,5)
        
        self.TextEntry = TextBox(self,CONVO)
        vbox.Add(self.TextEntry,0,wx.EXPAND,0)
        
        self.SetSizer(vbox)
        self.Layout()

class Conversation(scrolled.ScrolledPanel):
    def __init__(self, parent, CONVO, ID):
        scrolled.ScrolledPanel.__init__(self,parent,-1,style=wx.TAB_TRAVERSAL)
        self.MSGBox = wx.BoxSizer(wx.VERTICAL)
        self.CONVO = CONVO
        
        self.ID = ID
        pub.subscribe(self.LoadConversation,self.ID)
        self.LoadConversation()
        
    
    def LoadConversation(self, CONVO=None):
        if CONVO != None:
            self.CONVO = CONVO.data
        self.MSGBox.Clear(True)
        for msg in self.CONVO:
            MessageBox = ConvoMsg(self,msg)
            self.MSGBox.Add(MessageBox,0,wx.EXPAND|wx.LEFT|wx.RIGHT,0)
            MessageBox.msg.Wrap(self.Parent.Parent.GetSize()[0]-50)
        Globals.Voice._Message__messages_post('mark', self.ID, read=1)
        self.SetSizer(self.MSGBox)
        self.SetAutoLayout(1)
        self.SetupScrolling(scrollToTop=False)
        self.Scroll(-1,999999)
            

class TextBox(wx.Panel):
    def __init__(self, parent, CONVO, *args, **kws):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY,style=wx.BORDER_SUNKEN)
        self.CONVO = CONVO
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.TextEntry = wx.TextCtrl(self,style=wx.TE_MULTILINE)
        self.TextEntry.Bind(wx.EVT_KEY_DOWN, self.onKeyPress)
        hbox.Add(self.TextEntry,5,wx.EXPAND|wx.ALL,5)
        
        self.SendButton = wx.Button(self, 2, "Send")
        self.SendButton.Bind(wx.EVT_BUTTON, self.Send)
        hbox.Add(self.SendButton,1,wx.EXPAND|wx.ALL,5)
        
        self.SetSizer(hbox)
        self.Layout()
    
    def onKeyPress(self, event=None):
        keycode = event.GetKeyCode()
        shift = event.ShiftDown()
        if shift and keycode == wx.WXK_RETURN or keycode == wx.WXK_NUMPAD_ENTER:
            self.Send()
        else:
            event.Skip()
    
    def Send(self, event=None):
        text = self.TextEntry.GetValue()
        if text == "":
            return
        Globals.Voice.send_sms(self.CONVO[0]["number"], text)
        self.TextEntry.Clear()
        wx.CallAfter(pub.sendMessage,"ThreadForReLoadFolder",data=None)
        
