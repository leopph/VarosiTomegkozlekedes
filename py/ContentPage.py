import tkinter

class ContentPage(tkinter.Frame):
    def __init__(self, data, *args, **kwargs):
        tkinter.Frame.__init__(self, *args, **kwargs)
        self.data = data
