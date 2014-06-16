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


class Notify(Thread):
    def __init__(self):
        Thread.__init__(self)
        
        self.start()
    
    def run(self):
        if pynotify:
            self.runPynotifyVersion()
        else:
            runToasterVersion()
            
    def runPynotifyVersion(self):
        if pynotify.init("GoogleVoice"):
            n = pynotify.Notification("Google Voice Linux Client",
                                        "You have a meeting in 10 minutes.")
            n.set_urgency(pynotify.URGENCY_NORMAL)
            #n.add_action("default", "Default Action", self.RequestUser)
            
            if not n.show():
                print "Failed to send notification"
        
    
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
