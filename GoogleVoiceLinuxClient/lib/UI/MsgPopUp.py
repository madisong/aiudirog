import wx
from lib.Tools.Globals import *
from lib.UI.ConvoMsg import *
import  wx.lib.scrolledpanel as scrolled
from wx.lib.pubsub import setupv1
from wx.lib.pubsub import Publisher as pub

class MsgPopUp(wx.Frame):
    def __init__(self, parent=None, CONVO=None, *args, **kw):
        wx.Frame.__init__(self, parent=parent, id=wx.ID_ANY)
        
        self.ConvoPanel = MainConvoPanel(self,CONVO)
        self.Layout()
        
        
    def LoadConvo(self,event=None):
        self.ConvoPanel.LoadConversation()
        self.Layout()
        
    
class MainConvoPanel(wx.Panel):
    def __init__(self, parent, CONVO, *args, **kws):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY,style=wx.BORDER_SUNKEN)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        self.Conversation = Conversation(self,CONVO)
        vbox.Add(self.Conversation,5,wx.EXPAND|wx.LEFT|wx.RIGHT,5)
        
        self.TextEntry = TextBox(self,CONVO)
        vbox.Add(self.TextEntry,0,wx.EXPAND,0)
        
        self.SetSizer(vbox)
        self.Layout()

class Conversation(scrolled.ScrolledPanel):
    def __init__(self, parent, CONVO):
        scrolled.ScrolledPanel.__init__(self,parent,-1,style=wx.TAB_TRAVERSAL)
        self.MSGBox = wx.BoxSizer(wx.VERTICAL)
        self.CONVO = CONVO
        
        self.ID = CONVO[0]['id']
        pub.subscribe(self.ReLoad,str(self.ID))
        print self.ID
        self.LoadConversation()
        
        self.SetSizer(self.MSGBox)
        self.SetAutoLayout(1)
        self.SetupScrolling()
    
    def LoadConversation(self, CONVO=None):
        if CONVO != None:
            self.CONVO = CONVO
        self.MSGBox.Clear(True)
        for msg in self.CONVO:
            MessageBox = ConvoMsg(self,msg)
            self.MSGBox.Add(MessageBox,0,wx.EXPAND|wx.LEFT|wx.RIGHT,5)
            MessageBox.msg.Wrap(self.Parent.Parent.GetSize()[0]-30)
            
    def ReLoad(self,data=None):
        print True
        self.CONVO = data.data
        
        self.LoadConversation()

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
    
    def Send(self, event=None):
        print Globals.userdata
        #Globals.Voice.send_sms(phoneNumber, self.TextEntry.GetValue())
        
