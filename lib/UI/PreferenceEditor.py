import wx
from wx import ColourPickerCtrl as CPC
from wx import EVT_COLOURPICKER_CHANGED as evt_color
from lib.Tools.Globals import *
import  wx.lib.scrolledpanel as scrolled
from wx.lib.pubsub import setupv1
from wx.lib.pubsub import Publisher as pub
from lib.Tools.ExtraFunctions import *

class PreferenceEditor(wx.Dialog):
    def __init__(self, parent=None, *args, **kw):
        wx.Dialog.__init__(self, parent=None, id=wx.ID_ANY, size=(450,500))
        
        self.Panel = Options(self)
        self.SetTitle("Preferences")
        
        self.Layout()
        
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
        self.Show()
        
        
    def OnClose(self, event):
        self.Destroy()
    
    
class Options(scrolled.ScrolledPanel):
    def __init__(self, parent):
        scrolled.ScrolledPanel.__init__(self,parent,-1,style=wx.TAB_TRAVERSAL)
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        
        Windows= [("MainFrameBackgroundColor","Message List Background Color"),
                  ("BoxMessage","Conversation List Element Background"),
                  ("BoxMessageTEXT","Conversation List Element Text"),
                  ("ConvoMsgME","Conversation Window- Your Message Backgrounds"),
                  ("ConvoMsgMETEXT","Conversation Window- Your Message Text"),
                  ("ConvoMsgYOU","Conversation Window- Their Message Backgrounds"),
                  ("ConvoMsgYOUTEXT","Conversation Window- Their Message Text")]
        for name, text in Windows:
            Sizer = wx.BoxSizer(wx.HORIZONTAL)
            Button = CPC(self,name=name)
            Button.Bind(evt_color, self.SendColorChange)
            
            try: 
                Button.SetColour(GetTupleFromString(Globals.INI.get("MAIN",name)))
            except:
                pass
            
            Sizer.Add(Button,0,wx.ALL,5)
            
            T = wx.StaticText(self, -1, text)
            Sizer.Add(T,0,wx.ALL,5,wx.ALIGN_CENTER_VERTICAL)
            MainSizer.Add(Sizer,0,wx.EXPAND|wx.ALL,0)
            
        self.SetSizer(MainSizer)
        self.SetAutoLayout(1)
        self.SetupScrolling()
        
    def SendColorChange(self, event):
        color = event.GetColour()
        obj = event.GetEventObject()
        Globals.INI.set("MAIN", obj.Name, color)
        with open(Globals.ini_path, "w+") as ini:
            Globals.INI.write(ini)
        wx.CallAfter(pub.sendMessage,obj.Name,data=color)