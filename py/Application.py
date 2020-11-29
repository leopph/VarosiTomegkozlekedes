import tkinter
import Header
import DataInsert
import Home
import Login
import Register
import RouteResults
import Search
import StopDetails
import DataUpdate
import DataDelete
from typing import Union


class App(tkinter.Tk):
    def __init__(self, dbhost = "localhost", dbname = "varosi_tomegkozlekedes", dbuser = "root", dbpwd = "", *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.geometry("1280x720")
        self.minsize(960, 540)
        self.title("Városi Tömegközlekedés")
        self["bg"] = "dark slate grey"

        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 2)
        self.rowconfigure(1, weight = 98)

        self.dbhost = dbhost
        self.dbname = dbname
        self.dbuser = dbuser
        self.dbpwd = dbpwd

        self.user = None

        self.header = Header.Header(self, bg = "purple3")
        self.header.grid(row = 0, sticky = "NESW")

        self.content_pages = {
                                Home.Home,
                                Login.LoginPage,
                                Register.RegisterPage,
                                Search.SearchResults,
                                RouteResults.RouteResults,
                                StopDetails.StopDetails,
                                DataInsert.DataInsertPage,
                                DataUpdate.DataUpdatePage,
                                DataDelete.DataDeletePage
                            }

        self.loaded_pages = list()

        self.current_page = None
        self.load_new_page(Home.Home, None)

        self.header.backbutton["state"] = "disabled"
        self.header.nextbutton["state"] = "disabled"

        
    def load_new_page(self, page: type, data: Union[dict, list, None]):
        if page in self.content_pages:
            if self.current_page is not None and self.loaded_pages.index(self.current_page) != len(self.loaded_pages) - 1:
                del self.loaded_pages[self.loaded_pages.index(self.current_page) + 1:]

            self.current_page = page(data, self, bg=self["bg"])
            self.current_page.grid(row = 1, sticky = "NESW")
            self.loaded_pages.append(self.current_page)

            self.header.backbutton["state"] = "normal"
            self.header.nextbutton["state"] = "disabled"

    
    def load_previous_page(self):
        current_index = self.loaded_pages.index(self.current_page)

        if current_index - 1 >= 0:
            self.current_page = self.loaded_pages[current_index - 1]
            self.current_page.tkraise()

            self.header.backbutton["state"] = "disabled" if current_index - 1 == 0 else "normal"
            self.header.nextbutton["state"] = "normal"


    def load_next_page(self):
        current_index = self.loaded_pages.index(self.current_page)

        if current_index + 1 < len(self.loaded_pages):
            self.current_page = self.loaded_pages[current_index + 1]
            self.current_page.tkraise()

            self.header.backbutton["state"] = "normal"
            self.header.nextbutton["state"] = "disabled" if current_index + 1 == len(self.loaded_pages) - 1 else "normal"


    def reload_existing_pages(self):
        for page in self.loaded_pages:
            page.refresh()
