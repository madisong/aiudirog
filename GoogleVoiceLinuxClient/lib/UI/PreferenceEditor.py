import wx
from wx import ColourPickerCtrl as CPC
from wx import EVT_COLOURPICKER_CHANGED as evt_color
from Globals 
import  wx.lib.scrolledpanel as scrolled
from wx.lib.pubsub import setupv1
from wx.lib.pubsub import Publisher as pub

class PreferenceEditor(wx.Dialog):
    def __init__(self, parent=None, *args, **kw):
        wx.Dialog.__init__(self, parent=None, id=wx.ID_ANY, size=(450,500))
        
        self.Panel = Options(self,CONVO,ID)
        
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
        self.Layout()
        
        

    def OnClose(self, event):
        Globals.OpenConvos.remove(self.ID)
        event.Skip()
    
    
    
class Options(scrolled.ScrolledPanel):
    def __init__(self, parent):
        scrolled.ScrolledPanel.__init__(self,parent,-1,style=wx.TAB_TRAVERSAL)
        MainSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        Text = wx.BoxSizer(wx.VERTICAL)
        Buttons = wx.BoxSizer(wx.VERTICAL)
        MainSizer.Add(Text,0,wx.EXPAND|wx.ALL,0)
        MainSizer.Add(Buttons,0,wx.EXPAND|wx.ALL,0)
        
        MainFrameBackgroundColor = CPC(self)
        MainFrameBackgroundColor.Bind(evt_color, self.MainFrameBG)
        Buttons.Add(MainFrameBackgroundColor,0,wx.EXPAND|wx.ALL,0)
        
        MainFrameBackgroundText = wx.StaticText(self, -1, "Message List Background Color")
        Text.Add(MainFrameBackgroundText,0,wx.EXPAND|wx.ALL,0)
        
        self.SetSizer(MainSizer)
        self.SetAutoLayout(1)
        self.SetupScrolling()