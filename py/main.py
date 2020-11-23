import tkinter
import tkinter.messagebox
import mysql.connector




class ContentPage(tkinter.Frame):
    def __init__(self, data, *args, **kwargs):
        tkinter.Frame.__init__(self, *args, **kwargs)
        self.data = data




class Home(ContentPage):
    def __init__(self, data, *args, **kwargs):
        ContentPage.__init__(self, data, *args, **kwargs)
        self.label = tkinter.Label(self, text = "home")
        self.label.pack()




class SearchResults(ContentPage):
    def __init__(self, data, *args, **kwargs):
        ContentPage.__init__(self, data, *args, **kwargs)

        self.label = tkinter.Label(self, text = data["from"] + " - " + data["to"], font = ("", 32))
        self.label.pack(side = "top")

        for route, timestamps in data["results"].items():
            for timestamp in timestamps:
                label = tkinter.Label(self, text = str(route) + " " + str(timestamp))
                label.pack()




class Header(tkinter.Frame):
    def __init__(self, *args, **kwargs):
        tkinter.Frame.__init__(self, *args, **kwargs)

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)
        self.columnconfigure(2, weight = 2)
        self.columnconfigure(3, weight = 4)
        self.columnconfigure(4, weight = 2)
        self.columnconfigure(5, weight = 4)
        self.columnconfigure(6, weight = 1)


        self._backbutton = tkinter.Button(self, text = "Vissza", command = self.master.load_previous_page)
        self._backbutton.grid(row = 0, column = 0, sticky = "NESW")

        self._nextbutton = tkinter.Button(self, text = "Előre", command = self.master.load_next_page)
        self._nextbutton.grid(row = 0, column = 1, sticky = "NESW")

        self.from_stop_label = tkinter.Label(self, text = "Honnan:", bg = self["bg"])
        self.from_stop_label.grid(row = 0, column = 2, sticky = "E")

        self.from_stop = tkinter.Entry(self)
        self.from_stop.grid(row = 0, column = 3, sticky = "W")

        self.to_stop_label = tkinter.Label(self, text = "Hová:", bg = self["bg"])
        self.to_stop_label.grid(row = 0, column = 4, sticky = "E")

        self.to_stop = tkinter.Entry(self)
        self.to_stop.grid(row = 0, column = 5, sticky = "W")

        self.send_button = tkinter.Button(self, text = "Keresés", command = self.search)
        self.send_button.grid(row = 0, column = 6)

    
    @property
    def backbutton(self):
        return self._backbutton

    @property
    def nextbutton(self):
        return self._nextbutton


    def search(self):
        if self.from_stop.get() == "" or self.to_stop.get() == "":
            tkinter.messagebox.showwarning(title = "Figyelem!", message = "Kérem adja meg az indulási- és célállomását!")

        else:
            connection = mysql.connector.connect(host = dbhost, database = dbname, user = dbuser, password = dbpwd)
            cursor = connection.cursor()

            monster_sql = '''select indul.vonal_nev, ADDTIME(indul.mikor, alkerdes3.mikor) from indul
                    inner join (select menetrend.vonal, menetrend.visszamenet, menetrend.mikor from menetrend
                    inner join (select vonal, visszamenet, mikor from menetrend where megallo_nev = %s) as alkerdes1 on alkerdes1.vonal = menetrend.vonal and menetrend.visszamenet = alkerdes1.visszamenet
                    inner join (select vonal, visszamenet, mikor from menetrend where megallo_nev = %s) as alkerdes2 on alkerdes2.vonal = menetrend.vonal and menetrend.visszamenet = alkerdes2.visszamenet
                    where megallo_nev = %s
                    and menetrend.vonal in (select DISTINCT vonal from menetrend where megallo_nev = %s)
                    and alkerdes1.mikor < alkerdes2.mikor) as alkerdes3 on alkerdes3.vonal = indul.vonal_nev and alkerdes3.visszamenet = indul.visszamenet'''

            cursor.execute(operation = monster_sql, params = (self.from_stop.get(), self.to_stop.get(), self.from_stop.get(), self.to_stop.get()))
            rows = cursor.fetchall()

            if not rows:
                tkinter.messagebox.showerror(title = "Hiba", message = "Ezen az útvonalon nem jár egy járat sem!")

            else:
                data = {"from": self.from_stop.get(), "to": self.to_stop.get(), "results": dict()}

                for row in rows:
                    if row[0] not in data["results"]:
                        data["results"][row[0]] = list()
                    data["results"][row[0]].append(row[1]) 

                self.master.load_new_page("SearchResults", data)

            connection.close()

            self.from_stop.delete(0, "end")
            self.to_stop.delete(0, "end")




class App(tkinter.Tk):
    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.geometry("640x360")
        self.title("Városi Tömegközlekedés")

        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 2)
        self.rowconfigure(1, weight = 98)

        self.header = Header(self, bg = "grey")
        self.header.grid(row = 0, sticky = "NESW")

        self.content_pages = ["Home", "SearchResults"]
        self.loaded_pages = list()

        self.current_page = None
        self.load_new_page("Home", dict())

        self.header.backbutton["state"] = "disabled"
        self.header.nextbutton["state"] = "disabled"

        
    def load_new_page(self, page: str, data: dict):
        if page in self.content_pages:
            self.current_page = globals()[page](data, self)
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
            self.header.nextbutton["state"] = "disabled" if current_index + 1 == len(self.loaded_pages) -1 else "normal"




if __name__ == "__main__":
    dbhost = "localhost"
    dbname = "varosi_tomegkozlekedes"
    dbuser = "root"
    dbpwd = ""

    App().mainloop()