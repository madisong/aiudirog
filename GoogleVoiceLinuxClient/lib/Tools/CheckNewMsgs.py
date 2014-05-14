import wx
from lib.Tools.Globals import *
from lib.Tools.Notify import *
from threading import Thread
from wx.lib.pubsub import setupv1
from wx.lib.pubsub import Publisher as pub
from time import sleep
try:
    from json import loads
except ImportError:
    from simplejson import loads
try:
    from urllib2 import Request,urlopen
except ImportError:
    from urllib.request import Request,urlopen

#Check for new messages in a seperate thread.
class CheckNewMsgs(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.start()
        
    def run(self):
        CurrentUnreadCount = 0
        LastUnreadCount = 0
        while True:
            try:
                #Download unread counts from Google Voice API
                unread = loads(urlopen(Request("https://www.google.com/voice/request/unread")).read())
                CurrentUnreadCount = unread["unreadCounts"][Globals.CurrentFolder]
                #If messages have been checked and read, load those changes
                if CurrentUnreadCount < LastUnreadCount:
                    LastUnreadCount = CurrentUnreadCount
                if CurrentUnreadCount!=0 and LastUnreadCount!=CurrentUnreadCount:
                        print "New Messages!"
                        #Display notification
                        wx.CallAfter(Notify)
                        #Reload all conversations
                        wx.CallAfter(pub.sendMessage,"ThreadForReLoadFolder",data=None)
                        LastUnreadCount = CurrentUnreadCount
            except:
                pass
                #Eventually a pop-up to say there was no internet connection.
            sleep(5)
