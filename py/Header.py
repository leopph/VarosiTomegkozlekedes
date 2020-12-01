import tkinter
import tkinter.ttk
import tkinter.messagebox
import mysql.connector
import Home
import Search




class Header(tkinter.Frame):
    def __init__(self, *args, **kwargs):
        tkinter.Frame.__init__(self, *args, **kwargs)

        self.query_for_stops()

        self._backbutton = tkinter.Button(self, text = "Vissza", command = self.master.load_previous_page, bg = "DarkOliveGreen3")
        self._backbutton.grid(row = 0, column = 0)

        self._nextbutton = tkinter.Button(self, text = "Előre", command = self.master.load_next_page, bg = "DarkOliveGreen3")
        self._nextbutton.grid(row = 0, column = 1)

        tkinter.Button(self, text = "Főoldal", command = lambda: self.master.load_new_page(Home.Home, None), bg = "DarkOliveGreen3").grid(row = 0, column = 2)
        tkinter.Label(self, text = "Honnan:", bg = self["bg"], fg = "snow", font = ("", 10)).grid(row = 0, column = 3)

        self.from_stop = tkinter.ttk.Combobox(self)
        self.from_stop.config(postcommand=self.update_menus, width=max(len(stop) for stop in self.stops), state="readonly")
        self.from_stop.grid(row=0, column=4)
        self.from_stop.set("Válasszon megállót!")

        tkinter.Label(self, text = "Hová:", bg = self["bg"], fg = "snow", font = ("", 10)).grid(row = 0, column = 5)

        self.to_stop = tkinter.ttk.Combobox(self)
        self.to_stop.config(postcommand=self.update_menus, width=max(len(stop) for stop in self.stops), state="readonly")
        self.to_stop.grid(row=0, column=6)
        self.to_stop.set("Válasszon megállót!")

        tkinter.Button(self, text = "Keresés", command = self.search, bg = "thistle3").grid(row = 0, column = 7)

    
    @property
    def backbutton(self):
        return self._backbutton

    @property
    def nextbutton(self):
        return self._nextbutton


    def update_menus(self):
        self.query_for_stops()
        self.from_stop.config(values=sorted(self.stops.keys()), width=max(len(stop) for stop in self.stops))
        self.to_stop.config(values=sorted(self.stops.keys()), width=max(len(stop) for stop in self.stops))

    def query_for_stops(self):
        connection = mysql.connector.connect(host=self.master.dbhost, database=self.master.dbname, user=self.master.dbuser, password=self.master.dbpwd)
        cursor = connection.cursor()
        cursor.execute("SELECT nev, hely FROM megallo WHERE id IN(SELECT DISTINCT megallo_id FROM megall)")
        self.stops: dict[str, int] = {str(stop[0]) + " (" + str(stop[1]) + ")": stop[0] for stop in cursor.fetchall()}
        connection.close()


    def search(self):
        if self.from_stop.get() not in self.stops or self.to_stop.get() not in self.stops:
            tkinter.messagebox.showwarning(title = "Figyelem!", message = "Kérem adja meg az indulási- és célállomását!")

        else:
            self.focus_set()

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

            # Utólagos okosság, a fentebbi szükségtelenül bonyolult, ez ugyanazt csinálja:
            '''select indul.vonal_nev, indul.visszamenet, indul.mikor, alkerdes1.mikor, jarmu.tipus_nev from indul
                inner join jarmu on jarmu.rendszam = indul.rendszam
                inner join (select menetrend.vonal, menetrend.visszamenet, menetrend.mikor from menetrend
                inner join (select vonal, visszamenet, mikor from menetrend where megallo_nev = %s) as alkerdes2 on alkerdes2.vonal = menetrend.vonal and menetrend.visszamenet = alkerdes2.visszamenet
                where menetrend.megallo_nev = %s and menetrend.mikor < alkerdes2.mikor) as alkerdes1 on alkerdes1.vonal = indul.vonal_nev and alkerdes1.visszamenet = indul.visszamenet
                order by addtime(indul.mikor, alkerdes1.mikor)'''
            # A különbség a paramétersorrend

            cursor.execute(operation = monster_sql, params = (self.stops[self.from_stop.get()], self.stops[self.to_stop.get()], self.stops[self.from_stop.get()], self.stops[self.to_stop.get()]))
            rows = cursor.fetchall()

            if not rows:
                tkinter.messagebox.showerror(title = "Hiba", message = "Ezen az útvonalon nem jár egy járat sem!")

            else:
                data = {"from": self.stops[self.from_stop.get()], "to": self.stops[self.to_stop.get()], "results": dict()}

                for row in rows:
                    if row[0] not in data["results"]:
                        data["results"][row[0]] = list()
                    data["results"][row[0]].append((row[1], row[2], row[3], row[4]))

                self.master.load_new_page(Search.SearchResults, data)

            connection.close()

            self.from_stop.set("Válasszon megállót!")
            self.to_stop.set("Válasszon megállót!")
