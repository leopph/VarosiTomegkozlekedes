import tkinter
import ContentPage


class DataUpdatePage(ContentPage.ContentPage):
    def __init__(self, data, *args, **kwargs):
        ContentPage.ContentPage.__init__(self, data, *args, **kwargs)

        self.title_frame = None
        self.content_frame = None

        self.refresh()


    def refresh(self):
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 9)
        self.columnconfigure(0, weight = 1)
