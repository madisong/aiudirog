import wx
from lib.Tools.Globals import *
from threading import Thread
from lib.Tools.pygooglevoicepatches import *
import googlevoice as gv
import BeautifulSoup
from wx.lib.pubsub import setupv1
from wx.lib.pubsub import Publisher as pub
import re

class GetNewMsgs(Thread):
    def __init__(self,runwhat,arg=None):
        Thread.__init__(self)
        self.runwhat = runwhat
        self.arg = arg
        self.start()
        
    def run(self):
        getattr(self, self.runwhat)()
        
    def LoadFolder(self):
        getattr(Globals.Voice, self.arg)()
        
        tmpfolder = fetchfolderpage(Globals.Voice,self.arg,1)
        tmpfolder()
        Convos = self.extractsms(tmpfolder.html)
        wx.CallAfter(pub.sendMessage,"LoadFolder",data=Convos)
        
    def ReLoadFolder(self):
        size = len(self.arg)
        while size%10 != 0:
            size += 1
        pages = size/10
        Convos = []
        
        for x in range(pages):
            tmpfolder = fetchfolderpage(Globals.Voice,Globals.CurrentFolder,x)
            tmpfolder()
            tmpconvo = self.extractsms(tmpfolder.html)
            Convos += tmpconvo
            
        wx.CallAfter(pub.sendMessage,"ReLoadFolder",data=Convos)
    
    def LoadMoreMessages(self):
        size = len(self.arg)
        page = size/10+1
        
        tmpfolder = fetchfolderpage(Globals.Voice,Globals.CurrentFolder,page)
        tmpfolder()
        tmpconvo = self.extractsms(tmpfolder.html)
        self.arg += tmpconvo
        
        wx.CallAfter(pub.sendMessage,"LoadMoreMessages",data=self.arg)
    
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
            number = conversation.findAll(attrs={"class" : "gc-message-type"})
            if len(number) == 0:
                number = conversation.findAll(attrs={"class" : "gc-nobold"})
            number = number[0].string
            number = re.sub('[!@#$A-z+()\s-]', '', number)
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
                    if cl == "text":
                        msgitem[cl] = msgitem[cl].replace("&lt;3", "<3")
                msgitem["number"] = number
                tmp.append(msgitem)                    # add msg dictionary to list
            Convos.append(tmp)
        return Convos
