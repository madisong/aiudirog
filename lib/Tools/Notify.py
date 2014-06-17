import wx
from lib.Tools.Globals import *
from threading import Thread
from wx import GetClientDisplayRect as GCDR
try: import pynotify
except:
    import wx.lib.agw.toasterbox as TB
try:
    import pygame.mixer as mixer
    mixer.init(44100)
    mixer.music.load('Yah.wav')
except:
    mixer = None
import os

class Notify(Thread):
    """
    This thread will notify the user of any new messages. On a system that has
    pynotify, it will use that to notify the user via the the system 
    notifications. Otherwise it will use toasaterbox, which is a notification
    system built into wxpython.
    """
    def __init__(self, convos):
        Thread.__init__(self)
        self.msg = convos[0][-1]
        if self.msg['from'][:-1] == "Me":
            return
        self.start()
    
    def run(self):
        if pynotify:
            self.runPynotifyVersion()
        else:
            runToasterVersion()
            
    def runPynotifyVersion(self):
        if pynotify.init("GoogleVoice"):
            iconImage = "file://"+os.path.join(Globals.path, "resources",
                                                "google-voice-icon.png")
            n = pynotify.Notification("Google Voice Client: New Messages",
                              "Most Recent: {0}\n{1}".format(
                              self.msg['from'][:-1],self.msg['text']),iconImage)
            n.set_urgency(pynotify.URGENCY_NORMAL)
            
            if not n.show():
                print "Failed to send notification"
            self.PlaySound()
    
    def runToasterVersion(self):
        self.toaster = TB.ToasterBox(Globals.Frame, tbstyle=TB.TB_COMPLEX)
        self.toaster.SetPopupPauseTime(5000)

        tbpanel = self.toaster.GetToasterBoxWindow()
        panel = wx.Panel(tbpanel, -1, style=wx.BORDER_RAISED)
        sizer = wx.BoxSizer(wx.VERTICAL)

        button = wx.Button(panel, wx.ID_ANY, "Google Voice:\n\nNew Messages")
        button.Bind(wx.EVT_BUTTON,self.RequestUser)
        sizer.Add(button, 0, wx.EXPAND)

        panel.SetSizer(sizer)
        panel.SetBackgroundColour("#AFEEEE")
        self.toaster.AddPanel(panel)

        wx.CallAfter(self.toaster.Play)
        self.PlaySound()
        
    def PlaySound(self):
        if mixer:
            try: mixer.music.play() 
	    except:
               mixer.init(44100)
               mixer.music.load('Yah.wav')
               mixer.music.play() 
    
    def RequestUser(self, event=None):
        print True
        try: Globals.Frame.RequestUserAttention(1)
        except: pass
        try: Globals.Frame.Raise()
        except: pass
