import  wx
import  wx.lib.scrolledpanel as scrolled
from lib.UI.BoxMessage import *
from lib.Tools.Globals import *
import googlevoice

class MsgsPanel(scrolled.ScrolledPanel):
    def __init__(self, parent):
        scrolled.ScrolledPanel.__init__(self,parent,-1,style=wx.TAB_TRAVERSAL)
        self.MSGBox = wx.BoxSizer(wx.VERTICAL)
        self.CurrentBox = []
        self.LoginScreen()
        self.SetSizer(self.MSGBox)
        self.SetAutoLayout(1)
        self.SetupScrolling()

    def AddMessage(self, NAME, MSG):
        MSG = BoxMessage(self,NAME,MSG)
        self.CurrentBox.append(MSG)
        self.MSGBox.Add(MSG,0,wx.EXPAND|wx.ALL,5)
    
    def LoginScreen(self):
        VBOX = wx.BoxSizer(wx.VERTICAL)
        self.MSGBox.Add(VBOX,0,wx.EXPAND|wx.ALL,0)

        GoogleAccountTxt = wx.StaticText(self, -1, "Google Account:")
        self.GoogleAccount = wx.TextCtrl(self)
        VBOX.Add(GoogleAccountTxt,0,wx.EXPAND|wx.ALL,5)
        VBOX.Add(self.GoogleAccount,0,wx.EXPAND|wx.ALL,5)
        
        PasswordTxt = wx.StaticText(self, -1, "Password:")
        self.Password = wx.TextCtrl(self,style=wx.TE_PASSWORD)
        VBOX.Add(PasswordTxt,0,wx.EXPAND|wx.ALL,5)
        VBOX.Add(self.Password,0,wx.EXPAND|wx.ALL,5)
        
        submit = wx.Button(self, 1, "Submit")
        self.Bind(wx.EVT_BUTTON, self.Login, id=1)
        VBOX.Add(submit,0,wx.ALL,5)
        
        self.LoginScreenWidgets = [VBOX,GoogleAccountTxt,self.GoogleAccount,
                              PasswordTxt,self.Password,submit]
        
    def Login(self, instance):
        Password = self.Password.GetValue()
        GA = self.GoogleAccount.GetValue()
        if "@" not in GA:
            GA += "@gmail.com"
        try: Globals.Voice.login(GA,Password)
        except googlevoice.util.LoginError:
            #Window telling the user to try again.
            return
        del GA
        del Password
        for widget in self.LoginScreenWidgets:
            widget.Destroy()
