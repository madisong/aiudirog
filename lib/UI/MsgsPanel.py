import  wx
import  wx.lib.scrolledpanel as scrolled
from lib.UI.BoxMessage import *
from lib.Tools.Globals import *
from lib.Tools.CheckNewMsgs import *
from lib.Tools.GetNewMessages import *
import googlevoice as gv
import BeautifulSoup
from lib.Tools.pygooglevoicepatches import *
from wx.lib.pubsub import setupv1
from wx.lib.pubsub import Publisher as pub
import keyring
import keyring.util

from lib.Tools.BaseColorChangeObj import *

class MsgsPanel(scrolled.ScrolledPanel,BaseColorChangeObj):
    def __init__(self, parent):
        scrolled.ScrolledPanel.__init__(self,parent,-1,style=wx.TAB_TRAVERSAL)
        BaseColorChangeObj.__init__(self,"MainFrameBackgroundColor")
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        self.MSGBox = wx.BoxSizer(wx.VERTICAL)
        self.LoadMoreBox = wx.BoxSizer(wx.HORIZONTAL)
        
        MainSizer.Add(self.MSGBox,0,wx.EXPAND|wx.ALL,0)
        MainSizer.Add(self.LoadMoreBox,0,wx.EXPAND|wx.ALL,0)
        
        self.CurrentBox = []
        
        pub.subscribe(self.ReLoadFolder, "ReLoadFolder")
        pub.subscribe(self.ThreadForReLoadFolder, "ThreadForReLoadFolder")
        pub.subscribe(self.LoadFolder, "LoadFolder")
        pub.subscribe(self.LoadMoreMessages, "LoadMoreMessages")
        
        self.LoginScreen = LoginPanel(self)
        self.MSGBox.Add(self.LoginScreen,0,wx.EXPAND|wx.ALL,5)
        self.Bind(wx.EVT_BUTTON, self.Login, id=1)
        self.LoginScreen.Password.Bind(wx.EVT_TEXT_ENTER, self.Login)
        
        try: 
            self.SetBackgroundColour(GetTupleFromString(
                                             Globals.INI.get("MAIN","MainFrameBackgroundColor")))
        except: 
            self.SetBackgroundColour("#AFEEEE")
        
        self.SetSizer(MainSizer)
        self.SetAutoLayout(1)
        self.SetupScrolling()
    
    def Login(self, instance):
        Password = self.LoginScreen.Password.GetValue()
        GA = self.LoginScreen.GoogleAccount.GetValue()
        if self.LoginScreen.cb.GetValue():
            keyring.set_password('GoogleVoice','LastUser',GA+":"+Password)
        try: Globals.Voice.login(GA,Password)
        except gv.util.LoginError:
            Error = wx.MessageDialog(self, 
                                     "Login to Google Voice account failed. "\
                                     "Please check internet connection, "\
                                     "username, and password.",
                                     caption="Login Error", style=wx.ICON_ERROR)
            Error.ShowModal()
            return
        
        del GA
        del Password
        self.LoginScreen.Destroy()
        Globals.CurrentFolder = "inbox"
        GetNewMsgs("LoadFolder","inbox")
        LoadMore = wx.StaticText(self, -1, "Load More...")
        LoadMore.Bind(wx.EVT_LEFT_UP, self.ThreadForLoadMoreMessages)
        self.LoadMoreBox.Add(LoadMore,0,wx.EXPAND|wx.ALL,10)
        
        Refresh = wx.StaticText(self, -1, "Refresh")
        Refresh.Bind(wx.EVT_LEFT_UP, self.ThreadForReLoadFolder)
        self.LoadMoreBox.Add(Refresh,0,wx.EXPAND|wx.ALL,10)
        
        self.Layout()
    
    def CheckNew(self, event=None):
        CheckNewMsgs()
    
    def AddMessage(self, convo):
        MSG = BoxMessage(self,convo)
        self.CurrentBox.append(MSG)
        self.MSGBox.Add(MSG,0,wx.EXPAND|wx.ALL,5)
        
    def LoadFolder(self, data=None):
        self.Convos = data.data
        self.MSGBox.Clear(True)
        
        for convo in self.Convos:
            self.AddMessage(convo)
        self.Layout()
        self.SetAutoLayout(1)
        self.SetupScrolling()
        wx.CallAfter(self.CheckNew)
    
    def ThreadForLoadFolder(self, event=None):
        wx.CallAfter(GetNewMsgs,"LoadFolder")
    
    def ReLoadFolder(self, data=None):
        self.Convos = data.data
        self.MSGBox.Clear(True)
            
        for convo in self.Convos:
            self.AddMessage(convo)
            
        self.Layout()
        self.SetAutoLayout(1)
        self.SetupScrolling()
    
    def ThreadForReLoadFolder(self, event=None):
        if event.data == "Notify":
            notify = True
        else:
            notify = False
        wx.CallAfter(GetNewMsgs,"ReLoadFolder",self.Convos, notify)
    
    def LoadMoreMessages(self, data=None):
        self.MSGBox.Clear(True)
        self.Convos = data.data
        
        for convo in self.Convos:
            self.AddMessage(convo)
            
        self.Layout()
        self.SetAutoLayout(1)
        self.SetupScrolling()
    
    def ThreadForLoadMoreMessages(self, event=None):
        wx.CallAfter(GetNewMsgs,"LoadMoreMessages",self.Convos)
    
class LoginPanel(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY,
                          style=wx.BORDER_RAISED|wx.TAB_TRAVERSAL)
        self.VBOX = wx.BoxSizer(wx.VERTICAL)

        GoogleAccountTxt = wx.StaticText(self, -1, "Google Account:")
        self.GoogleAccount = wx.TextCtrl(self)
        self.VBOX.Add(GoogleAccountTxt,0,wx.EXPAND|wx.ALL,5)
        self.VBOX.Add(self.GoogleAccount,0,wx.EXPAND|wx.ALL,5)
        
        PasswordTxt = wx.StaticText(self, -1, "Password:")
        self.Password = wx.TextCtrl(self,
                                    style=wx.TE_PASSWORD|wx.TE_PROCESS_ENTER)
        
        self.VBOX.Add(PasswordTxt,0,wx.EXPAND|wx.ALL,5)
        self.VBOX.Add(self.Password,0,wx.EXPAND|wx.ALL,5)
        
        self.cb = wx.CheckBox(self, -1, 'Save Login Details?', (10, 10))
        self.cb.SetValue(True)
        self.VBOX.Add(self.cb, 0, wx.EXPAND|wx.ALL, 5)
        
        self.submit = wx.Button(self, 1, "Submit")
        
        self.VBOX.Add(self.submit,0,wx.ALL,5)
        
        userpass = keyring.get_password('GoogleVoice','LastUser')
        if userpass != None:
            userpass = userpass.split(":")
            self.GoogleAccount.SetValue(userpass[0])
            self.Password.SetValue(userpass[1])
        
        self.SetSizer(self.VBOX)
        
    
       
