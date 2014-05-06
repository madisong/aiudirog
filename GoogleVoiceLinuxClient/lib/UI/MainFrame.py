import wx

class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, 
                          size=(300,wx.GetDisplaySize()[1]))
        
        self.Show()


