import  wx
import  wx.lib.scrolledpanel as scrolled
from lib.UI.BoxMessage import *
from lib.Tools.Globals import *
import googlevoice as gv
import BeautifulSoup
from lib.Tools.pygooglevoicepatches import *

class MsgsPanel(scrolled.ScrolledPanel):
    def __init__(self, parent):
        scrolled.ScrolledPanel.__init__(self,parent,-1,style=wx.TAB_TRAVERSAL)
        self.MSGBox = wx.BoxSizer(wx.VERTICAL)
        self.CurrentBox = []
        self.CurrentFolder = None
        
        self.LoginScreen = LoginPanel(self)
        self.MSGBox.Add(self.LoginScreen,0,wx.EXPAND|wx.ALL,5)
        self.Bind(wx.EVT_BUTTON, self.Login, id=1)
        self.LoginScreen.Password.Bind(wx.EVT_TEXT_ENTER, self.Login)
        
        self.SetBackgroundColour("#FFD700")
        
        self.SetSizer(self.MSGBox)
        self.SetAutoLayout(1)
        self.SetupScrolling()
    
    def Login(self, instance):
        Password = self.LoginScreen.Password.GetValue()
        GA = self.LoginScreen.GoogleAccount.GetValue()
        if "@" not in GA:
            GA += "@gmail.com"
        try: Globals.Voice.login(GA,Password)
        except gv.util.LoginError:
            Error = wx.MessageDialog(self, 
                                     "Login to Google Voice account failed. "\
                                     "Please check internet connection, username, and password.",
                                     caption="Login Error", style=wx.ICON_ERROR)
            Error.ShowModal()
            return
        del GA
        del Password
        self.LoginScreen.Destroy()
        self.Layout()
        self.LoadFolder("inbox")

    def AddMessage(self, convo):
        MSG = BoxMessage(self,convo)
        self.CurrentBox.append(MSG)
        self.MSGBox.Add(MSG,0,wx.EXPAND|wx.ALL,5)
        
    def LoadFolder(self, folder):
        getattr(Globals.Voice, folder)()
        Convos = []
        totalsize = getattr(Globals.Voice, folder).data['totalSize']
        while totalsize%10 != 0:
            totalsize += 1
        
        for x in range(totalsize/10):
            tmpfolder = fetchfolderpage(Globals.Voice,folder, x)
            tmpfolder()
            tmpconvo = self.extractsms(tmpfolder.html)
            Convos += tmpconvo
            
        for convo in Convos:
            self.AddMessage(convo)
        self.Layout()
    
    def extractsms(self,htmlsms) :
        """
        extractsms  --  extract SMS messages from BeautifulSoup tree of Google Voice SMS HTML.

        Output is a list of dictionaries, one per message.
        """
        #   Extract all conversations by searching for a DIV with an ID at top level.
        tree = BeautifulSoup.BeautifulSoup(htmlsms)         # parse HTML into tree
        conversations = tree.findAll("div",attrs={"id" : True},recursive=False)
        Convos = []
        for conversation in conversations:
            #   For each conversation, extract each row, which is one SMS message.
            rows = conversation.findAll(attrs={"class" : "gc-message-sms-row"})
            tmp = []
            for row in rows :                               # for all rows
                #   For each row, which is one message, extract all the fields.
                msgitem = {"id" : conversation["id"]}       # tag this message with conversation ID
                spans = row.findAll("span",attrs={"class" : True}, recursive=False)
                for span in spans :                         # for all spans in row
                    cl = span["class"].replace('gc-message-sms-', '')
                    msgitem[cl] = (" ".join(span.findAll(text=True))).strip()   # put text in dict
                tmp.append(msgitem)                    # add msg dictionary to list
            Convos.append(tmp)
        return Convos
        
class LoginPanel(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY,
                          style=wx.BORDER_RAISED)
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
        
        self.submit = wx.Button(self, 1, "Submit")
        
        self.VBOX.Add(self.submit,0,wx.ALL,5)
        
        self.SetSizer(self.VBOX)
        
    
       
