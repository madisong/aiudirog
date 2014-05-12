import wx
from lib.Tools.Globals import *
from threading import Thread
try: from wx.lib.pubsub import Publisher as pub
except: 
    from wx.lib.pubsub import setuparg1
    from wx.lib.pubsub import pub
from time import sleep
try:
    from json import loads
except ImportError:
    from simplejson import loads
try:
    from urllib2 import Request,urlopen
except ImportError:
    from urllib.request import Request,urlopen

class CheckNewMsgs(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.start()
        
    def run(self):
        CurrentUnreadCount = 0
        LastUnreadCount = 0
        while True:
            unread = loads(urlopen(Request("https://www.google.com/voice/request/unread")).read())
            CurrentUnreadCount = unread["unreadCounts"][Globals.CurrentFolder]
            if CurrentUnreadCount!=0 and LastUnreadCount!=CurrentUnreadCount:
                    print "New Messages!"
                    wx.CallAfter(pub.sendMessage,"ReLoadFolder",data=None)
                    LastUnreadCount = CurrentUnreadCount
            sleep(5)
