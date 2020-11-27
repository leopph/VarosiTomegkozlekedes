import tkinter
import abc

class ContentPage(tkinter.Frame, abc.ABC):
    def __init__(self, data, *args, **kwargs):
        tkinter.Frame.__init__(self, *args, **kwargs)
        self.data = data


    @abc.abstractmethod
    def refresh(self) -> None:
        pass
