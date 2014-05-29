import wx
from wx import ColourPickerCtrl as CPC
from wx import EVT_COLOURPICKER_CHANGED as evt_color
from lib.Tools.Globals import *
import  wx.lib.scrolledpanel as scrolled
from wx.lib.pubsub import setupv1
from wx.lib.pubsub import Publisher as pub

class PreferenceEditor(wx.Dialog):
    def __init__(self, parent=None, *args, **kw):
        wx.Dialog.__init__(self, parent=None, id=wx.ID_ANY, size=(450,500))
        
        self.Panel = Options(self)
        self.SetTitle("Preferences")
        
        self.Layout()
        
        self.Show()
    
    
    
class Options(scrolled.ScrolledPanel):
    def __init__(self, parent):
        scrolled.ScrolledPanel.__init__(self,parent,-1,style=wx.TAB_TRAVERSAL)
        MainSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        Text = wx.BoxSizer(wx.VERTICAL)
        Buttons = wx.BoxSizer(wx.VERTICAL)
        MainSizer.Add(Text,0,wx.EXPAND|wx.ALL,0)
        MainSizer.Add(Buttons,0,wx.EXPAND|wx.ALL,0)
        
        Windows= [("MainFrameBackgroundColor","Message List Background Color"),
                  ("BoxMessage","Conversation List"),
                  ("ConvoMsgME","Conversation Window- Your Messages"),
                  ("ConvoMsgYOU","Conversation Window- Their Messages")]
        for name, text in Windows:
            Button = CPC(self,name=name)
            Button.Bind(evt_color, self.SendColorChange)
            Buttons.Add(Button,0,wx.EXPAND|wx.ALL,5)
            
            T = wx.StaticText(self, -1, text)
            Text.Add(T,0,wx.EXPAND|wx.ALL,5)
        
        self.SetSizer(MainSizer)
        self.SetAutoLayout(1)
        self.SetupScrolling()
        
    def SendColorChange(self, event):
        color = event.GetColour()
        obj = event.GetEventObject()
        Globals.INI.set("MAIN", obj.Name, color)
        with open(Globals.ini_path, "r+") as ini:
            Globals.INI.write(ini)
        wx.CallAfter(pub.sendMessage,obj.Name,data=color)