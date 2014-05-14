import wx
from wx.lib.pubsub import setupv1
from wx.lib.pubsub import Publisher as pub

        
        
class BaseColorChangeObj():
    """
    This class will give windows the ability to change color. 
    MUST be inherited by a wxWindow.
    """
    def __init__(self, Name):
        pub.subscribe(self.ChangeColor,Name)
        print True
    
    def ChangeColor(self, data):
        self.SetBackgroundColour(data.data)
        print True