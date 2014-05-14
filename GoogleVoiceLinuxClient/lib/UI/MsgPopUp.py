import wx
from lib.UI.ConvoMsg import *
import  wx.lib.scrolledpanel as scrolled
from wx.lib.pubsub import setupv1
from wx.lib.pubsub import Publisher as pub

class MsgPopUp(wx.Dialog):
    def __init__(self, parent=None, CONVO=None, *args, **kw):
        wx.Dialog.__init__(self, parent=parent, id=wx.ID_ANY,
                           style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        
        self.ConvoPanel = Conversation(self,CONVO)
        self.CONVO = CONVO
        self.Layout()
        
        
    def LoadConvo(self,event=None):
        self.ConvoPanel.LoadConversation()
        self.Layout()
        
    
        
        
class Conversation(scrolled.ScrolledPanel):
    def __init__(self, parent, CONVO):
        scrolled.ScrolledPanel.__init__(self,parent,-1,style=wx.TAB_TRAVERSAL)
        self.MSGBox = wx.BoxSizer(wx.VERTICAL)
        self.CONVO = CONVO
        
        self.ID = CONVO[0]['id']
        pub.subscribe(self.ReLoad, self.ID)
        
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
            MessageBox.msg.Wrap(self.Parent.GetSize()[0]-30)
            
    def ReLoad(self,data=None):
        self.CONVO = data
        self.LoadConversation()
