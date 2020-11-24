import tkinter
import tkinter.messagebox
import mysql.connector
import Home
import Search




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
        self.columnconfigure(7, weight = 1)


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

        self.home_button = tkinter.Button(self, text = "Főoldal", command = lambda: self.master.load_new_page(Home.Home, None), bg = "DarkOliveGreen3")
        self.home_button.grid(row = 0, column = 7)

    
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
            connection = mysql.connector.connect(host = self.master.dbhost, database = self.master.dbname, user = self.master.dbuser, password = self.master.dbpwd)
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

                self.master.load_new_page(Search.SearchResults, data)

            connection.close()

            self.from_stop.delete(0, "end")
            self.to_stop.delete(0, "end")