import wx
from threading import Thread
"""
There are two version of the publisher library in wxPython. Only one gets
put in the final execuatable. This attempts to load either to be safe.

The default version of publisher also changes based upon the version of 
wxPython installed.
"""
try: from wx.lib.pubsub import Publisher as pub
except: 
    print "Changing pub mode"
    from wx.lib.pubsub import setuparg1
    from wx.lib.pubsub import pub
    
import sched, time

class Globals:
    width = 100
    height = 600
    StopTimer = False

class MainWindow(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, title="Timer")
        self.panel = TimerPanel(self)
        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.Sizer)
        self.Sizer.Add(self.panel, 1, wx.ALL|wx.EXPAND, 5)
        self.Fit()
        self.Layout()

class TimerPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        TimerIsRunning = False
        #Make a timer controller
        HR = wx.StaticText(self,-1,"HR")
        MIN = wx.StaticText(self,-1,"MIN")
        SEC = wx.StaticText(self,-1,"SEC")
        
        StampSizer = wx.BoxSizer(wx.HORIZONTAL)
        StampSizer.SetMinSize((1,1))
        MainSizer.Add(StampSizer, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTRE_HORIZONTAL, 5)
        StampSizer.Add(HR, 1, wx.TOP|wx.LEFT|wx.RIGHT|wx.ALIGN_CENTRE_HORIZONTAL, 5)
        StampSizer.Add(MIN, 1, wx.TOP|wx.LEFT|wx.RIGHT|wx.ALIGN_CENTRE_HORIZONTAL, 5)
        StampSizer.Add(SEC, 1, wx.TOP|wx.LEFT|wx.RIGHT|wx.ALIGN_CENTRE_HORIZONTAL, 5)
        
        self.Hours = wx.SpinCtrl(self, -1,style=wx.TE_CENTRE, size=(50,-1))
        self.Hours.SetRange(0,999999)
        self.Min = wx.SpinCtrl(self, -1,style=wx.TE_CENTRE, size=(50,-1))
        self.Min.SetRange(0,60)
        self.Sec = wx.SpinCtrl(self, -1,style=wx.TE_CENTRE, size=(50,-1))
        self.Sec.SetRange(0,60)
        
        pub.subscribe(self.updateProgress, "update_gauge")
        
        TimerSizer = wx.BoxSizer(wx.HORIZONTAL)
        TimerSizer.SetMinSize((1,1))
        MainSizer.Add(TimerSizer, 0, wx.ALL|wx.EXPAND, 5)
        TimerSizer.Add(self.Hours, 1, wx.BOTTOM|wx.LEFT|wx.RIGHT|wx.EXPAND, 5)
        TimerSizer.Add(self.Min, 1, wx.BOTTOM|wx.LEFT|wx.RIGHT|wx.EXPAND, 5)
        TimerSizer.Add(self.Sec, 1, wx.BOTTOM|wx.LEFT|wx.RIGHT|wx.EXPAND, 5)
        
        self.Gauge = wx.Gauge(self, id=-1, range=100, size=(-1,900), style=wx.GA_VERTICAL)
        MainSizer.Add(self.Gauge, 1, wx.ALL|wx.EXPAND, 5)
        
        self.SetSizer(MainSizer)
        self.Fit()
        self.Layout()

    def StartTimer(self, event=None):
        time = 0
        try: time += self.Hours.GetValue()*3600
        except: pass
        try: time += self.Min.GetValue()*60
        except: pass
        try: time += self.Sec.GetValue()
        except: pass
    
        if TimerIsRunning:
            Globals.StopTimer = True
        

class TimerThread(Thread):
    def __init__(self, time):
        Thread.__init__(self)
        self.time = time
        self.start()
        self.scheduler = sched.scheduler(time.time, time.sleep)
        
    def run(self):
        self.scheduler.enter(1, 1, decrementtime, (self.scheduler,))
        
    def decrementtime(sc): 
        if Globals.StopTimer:
            Globals.StopTimer = False
            return
        
        self.scheduler.enter(1, 1, decrementtime, (self.scheduler,))


s.run()
        
app = wx.App(False)

Frame = MainWindow()
Frame.Show()
app.MainLoop()
        