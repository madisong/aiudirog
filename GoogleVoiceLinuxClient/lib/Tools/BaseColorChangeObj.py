import wx
from wx.lib.pubsub import setupv1
from wx.lib.pubsub import Publisher as pub

        
        
class BaseColorChangeObj():
    """
    This class will give windows the ability to change color. 
    MUST be inherited by a wxWindow.
    """
    def __init__(self, Name):
        #Subscribe to a change in background color
        pub.subscribe(self.ChangeColor,Name)
        #Subscribe to a change in msg or name color (BoxMessage and ConvoMsg)
        pub.subscribe(self.ChangeTextColor,Name+"TEXT")
    
    def ChangeColor(self, data):
        self.SetBackgroundColour(data.data)
    
    def ChangeTextColor(self, data):
        self.msg.SetForegroundColour(data.data)
        self.name.SetForegroundColour(data.data)
        self.time.SetForegroundColour(data.data)