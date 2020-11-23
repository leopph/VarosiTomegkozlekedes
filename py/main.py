import tkinter
import tkinter.messagebox
import mysql.connector



class Route:
    def __init__(self, name: str, is_returning: bool, type: str, dep_time = None):
        self._name = name
        self._is_returning = is_returning
        self.type = type
        self._dep_time = dep_time

    
    @property
    def name(self):
        return self._name

    @property
    def is_returning(self):
        return self._is_returning

    @property
    def departure(self):
        return self._dep_time




class Stop:
    def __init__(self, name: str, location: str):
        self._name = name
        self._location = location

    
    @property
    def name(self):
        return self._name

    @property
    def location(self):
        return self._location




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

        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 9)

        title_frame = tkinter.Frame(master = self, bg = self["bg"])
        title_frame.grid(row = 0, sticky = "NESW")

        title_frame.rowconfigure(0, weight = 1)
        title_frame.columnconfigure(0, weight = 1)

        tkinter.Label(master = title_frame, text = data["from"] + " - " + data["to"], font = (None, 24), bg = self["bg"]).grid(row = 0, column = 0, sticky = "NESW")
    

        result_frame = tkinter.Frame(master = self, bg = self["bg"])
        result_frame.grid(row = 1, sticky = "NESW")

        result_frame.columnconfigure(0, weight = 4)
        result_frame.columnconfigure(1, weight = 4)
        result_frame.columnconfigure(2, weight = 4)
        result_frame.columnconfigure(3, weight = 1)

        grid_row_count = 0
        for route_id, datalist in data["results"].items():
            for data in datalist:
                route = Route(route_id, data[0], data[3], data[1])

                tkinter.Label(result_frame, text = route.name, font = (None, 12), bg = "LightSkyBlue2").grid(row = grid_row_count, column = 0, sticky = "NESW")
                tkinter.Label(result_frame, text = route.type, font = (None, 12), bg = "LightSkyBlue2").grid(row = grid_row_count, column = 1, sticky = "NESW")
                tkinter.Label(result_frame, text = route.departure + data[2], font = (None, 12), bg = "LightSkyBlue2").grid(row = grid_row_count, column = 2, sticky = "NESW")
                tkinter.Button(result_frame, text = "Részletek", command = lambda route = route: self.route_details(route), bg = "dark slate blue", fg = "snow").grid(row = grid_row_count, column = 3, sticky = "NESW")

                grid_row_count += 1

    
    def route_details(self, route: Route):
        connection = mysql.connector.connect(host = dbhost, database = dbname, user = dbuser, password = dbpwd)
        cursor = connection.cursor()

        sql = '''select megallo.nev, megallo.hely, addtime(megall.mikor, indul.mikor) from megall
                inner join megallo on megall.megallo_id = megallo.id
                inner join indul on megall.visszamenet = indul.visszamenet and megall.vonal_nev = indul.vonal_nev
                where megall.vonal_nev = %s and megall.visszamenet = %s and indul.mikor = %s
                order by addtime(indul.mikor, megall.mikor)'''

        cursor.execute(operation = sql, params = (route.name, route.is_returning, route.departure))

        data = {"route": route, "stops": list()}

        for row in cursor.fetchall():
            data["stops"].append((Stop(row[0], row[1]), row[2]))

        connection.close()

        self.master.load_new_page("RouteResults", data)




class RouteResults(ContentPage):
    def __init__(self, data, *args, **kwargs):
        ContentPage.__init__(self, data, *args, **kwargs)

        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 9)


        title_frame = tkinter.Frame(self, bg = self["bg"])
        title_frame.grid(row = 0, column = 0, sticky = "NESW")

        title_frame.rowconfigure(0, weight = 1)
        title_frame.columnconfigure(0, weight = 1)

        tkinter.Label(title_frame, text = data["route"].name + " jelzésű " + data["route"].type, font = (None, 24), bg = self["bg"]).grid(row = 0, sticky = "NESW")

        result_frame = tkinter.Frame(self, bg = self["bg"])
        result_frame.grid(row = 1, sticky = "NESW")

        result_frame.columnconfigure(0, weight = 4)
        result_frame.columnconfigure(1, weight = 4)
        result_frame.columnconfigure(2, weight = 4)
        result_frame.columnconfigure(3, weight = 1)

        grid_row_count = 0
        for stop, time in data["stops"]:
            tkinter.Label(result_frame, text = time, font = (None, 12)).grid(row = grid_row_count, column = 0, sticky = "NESW")
            tkinter.Label(result_frame, text = stop.name, font = (None, 12)).grid(row = grid_row_count, column = 1, sticky = "NESW")
            tkinter.Label(result_frame, text = stop.location, font = (None, 12)).grid(row = grid_row_count, column = 2, sticky = "NESW")
            tkinter.Button(result_frame, text = "Részletek", font = (None, 12), command = lambda stop = stop: self.stop_details(stop)).grid(row = grid_row_count, column = 3, sticky = "NESW")

            grid_row_count += 1


    def stop_details(self, stop: Stop):
        print(stop.name)




class StopDetails:
    pass
          



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


        self._backbutton = tkinter.Button(self, text = "Vissza", command = self.master.load_previous_page, bg = "DarkOliveGreen3")
        self._backbutton.grid(row = 0, column = 0, sticky = "NESW")

        self._nextbutton = tkinter.Button(self, text = "Előre", command = self.master.load_next_page, bg = "DarkOliveGreen3")
        self._nextbutton.grid(row = 0, column = 1, sticky = "NESW")

        self.from_stop_label = tkinter.Label(self, text = "Honnan:", bg = self["bg"], fg = "snow", font = (None, 10))
        self.from_stop_label.grid(row = 0, column = 2, sticky = "E")

        self.from_stop = tkinter.Entry(self)
        self.from_stop.grid(row = 0, column = 3, sticky = "W")

        self.to_stop_label = tkinter.Label(self, text = "Hová:", bg = self["bg"], fg = "snow", font = (None, 10))
        self.to_stop_label.grid(row = 0, column = 4, sticky = "E")

        self.to_stop = tkinter.Entry(self)
        self.to_stop.grid(row = 0, column = 5, sticky = "W")

        self.search_button = tkinter.Button(self, text = "Keresés", command = self.search, bg = "thistle3")
        self.search_button.grid(row = 0, column = 6)

    
    @property
    def backbutton(self):
        return self._backbutton

    @property
    def nextbutton(self):
        return self._nextbutton


    def search(self):
        from_stop = self.from_stop.get().strip()
        to_stop = self.to_stop.get().strip()

        if from_stop == "" or to_stop == "":
            tkinter.messagebox.showwarning(title = "Figyelem!", message = "Kérem adja meg az indulási- és célállomását!")

        else:
            connection = mysql.connector.connect(host = dbhost, database = dbname, user = dbuser, password = dbpwd)
            cursor = connection.cursor()

            monster_sql = '''select indul.vonal_nev, indul.visszamenet, indul.mikor, alkerdes3.mikor, jarmu.tipus_nev from indul
                    inner join jarmu on jarmu.rendszam = indul.rendszam
                    inner join (select menetrend.vonal, menetrend.visszamenet, menetrend.mikor from menetrend
                    inner join (select vonal, visszamenet, mikor from menetrend where megallo_nev = %s) as alkerdes1 on alkerdes1.vonal = menetrend.vonal and menetrend.visszamenet = alkerdes1.visszamenet
                    inner join (select vonal, visszamenet, mikor from menetrend where megallo_nev = %s) as alkerdes2 on alkerdes2.vonal = menetrend.vonal and menetrend.visszamenet = alkerdes2.visszamenet
                    where megallo_nev = %s
                    and menetrend.vonal in (select DISTINCT vonal from menetrend where megallo_nev = %s)
                    and alkerdes1.mikor < alkerdes2.mikor) as alkerdes3 on alkerdes3.vonal = indul.vonal_nev and alkerdes3.visszamenet = indul.visszamenet
                    order by addtime(indul.mikor, alkerdes3.mikor)'''

            cursor.execute(operation = monster_sql, params = (from_stop, to_stop, from_stop, to_stop))
            rows = cursor.fetchall()

            if not rows:
                tkinter.messagebox.showerror(title = "Hiba", message = "Ezen az útvonalon nem jár egy járat sem!")

            else:
                data = {"from": from_stop, "to": to_stop, "results": dict()}

                for row in rows:
                    if row[0] not in data["results"]:
                        data["results"][row[0]] = list()
                    data["results"][row[0]].append((row[1], row[2], row[3], row[4]))

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

        self.header = Header(self, bg = "slate blue")
        self.header.grid(row = 0, sticky = "NESW")

        self.content_pages = ["Home", "SearchResults", "RouteResults"]
        self.loaded_pages = list()

        self.current_page = None
        self.load_new_page("Home", dict())

        self.header.backbutton["state"] = "disabled"
        self.header.nextbutton["state"] = "disabled"

        
    def load_new_page(self, page: str, data: dict):
        if page in self.content_pages:
            if self.current_page is not None and self.loaded_pages.index(self.current_page) != len(self.loaded_pages) - 1:
                del self.loaded_pages[self.loaded_pages.index(self.current_page) + 1:]

            self.current_page = globals()[page](data, self, bg = "snow")
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




if __name__ == "__main__":
    dbhost = "localhost"
    dbname = "varosi_tomegkozlekedes"
    dbuser = "root"
    dbpwd = ""

    App().mainloop()