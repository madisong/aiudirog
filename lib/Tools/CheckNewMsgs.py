import wx
from lib.Tools.Globals import *
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
        #Download contacts:
        try:
            userinfo = loads(urlopen(Request("https://www.google.com/voice/request/user")).read())
            Contacts = userinfo["contacts"]
            for c, value in Contacts.iteritems():
                name = value["name"].replace("#39;", "'").replace("&lt;3", "<3")
                Globals.Contacts[name] = value["phoneNumber"]
                Globals.ContactNames.append(name)
        except:
            pass
            #Eventually a pop-up to say there was no internet connection.
        CurrentUnreadCount = 0
        LastUnreadCount = 0
        while True:
            if Globals.DEAD == True:
                print "Thread is breaking"
                break
            try:
                #Download unread counts from Google Voice API
                unread = loads(urlopen(Request("https://www.google.com/voice/request/unread")).read())
                CurrentUnreadCount = unread["unreadCounts"][Globals.CurrentFolder]
                #If messages have been checked and read, load those changes
                if CurrentUnreadCount < LastUnreadCount:
                    LastUnreadCount = CurrentUnreadCount
                if CurrentUnreadCount!=0 and LastUnreadCount!=CurrentUnreadCount:
                        print "New Messages!"
                        #Reload all conversations
                        wx.CallAfter(pub.sendMessage,"ThreadForReLoadFolder",
                                                        data="Notify")
                        LastUnreadCount = CurrentUnreadCount
            except:
                pass
                #Eventually a pop-up to say there was no internet connection.
            for x in range(5):
                if Globals.DEAD == True:
                    print "Stop checking messages, closing thread."
                    break
                else:
                    sleep(1)
            
