import ContentPage
import tkinter
import Entity
import mysql.connector
import RouteResults




class StopDetails(ContentPage.ContentPage):
    def __init__(self, data, *args, **kwargs):
        ContentPage.ContentPage.__init__(self, data, *args, **kwargs)

        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 9)

        title_frame = tkinter.Frame(self, bg = self["bg"])
        title_frame.grid(row = 0, column = 0, sticky = "NESW")

        title_frame.columnconfigure(0, weight = 1)

        tkinter.Label(title_frame, text = data["stop"].name, font = ("", 24), bg = self["bg"], fg="snow").grid(row = 0, sticky = "NESW")
        tkinter.Label(title_frame, text = data["stop"].location, font = ("", 20), bg = self["bg"], fg="snow").grid(row = 1, sticky = "NESW")

        results_frame = tkinter.Frame(self, bg = self["bg"])
        results_frame.grid(row = 1, sticky = "NESW")

        results_frame.columnconfigure(0, weight = 8)
        results_frame.columnconfigure(1, weight = 4)
        results_frame.columnconfigure(2, weight = 4)
        results_frame.columnconfigure(3, weight = 1)
        results_frame.columnconfigure(4, weight = 8)


        tkinter.Label(master=results_frame, text="Járat", font=("", 16), bg=self["bg"], fg="snow").grid(row=0, column=1)
        tkinter.Label(master=results_frame, text="Időpont", font=("", 16), bg=self["bg"], fg="snow").grid(row=0, column=2)


        grid_row_count = 1
        for elem in data["routes"]:
           tkinter.Label(results_frame, text = elem["route"].name + " jelzésű " + elem["route"].type + " (" + elem["misc"][1].capitalize() + " felé)", font = ("", 12), bg=self["bg"], fg="snow").grid(row = grid_row_count, column = 1, sticky = "NESW")
           tkinter.Label(results_frame, text = elem["route"].departure + elem["misc"][0], font = ("", 12), bg=self["bg"], fg="snow").grid(row = grid_row_count, column = 2, sticky = "NESW")
           tkinter.Button(results_frame, text = "Részletek", bg = "dark slate blue", fg = "snow", command = lambda route = elem["route"]: self.route_details(route)).grid(row = grid_row_count, column = 3, sticky = "NESW")

           grid_row_count += 1


    def route_details(self, route):
        connection = mysql.connector.connect(host = self.master.dbhost, database = self.master.dbname, user = self.master.dbuser, password = self.master.dbpwd)
        cursor = connection.cursor()

        sql = '''select megallo.nev, megallo.hely, addtime(megall.mikor, indul.mikor) from megall
                inner join megallo on megall.megallo_id = megallo.id
                inner join indul on megall.visszamenet = indul.visszamenet and megall.vonal_nev = indul.vonal_nev
                where megall.vonal_nev = %s and megall.visszamenet = %s and indul.mikor = %s
                order by addtime(indul.mikor, megall.mikor)'''

        cursor.execute(operation = sql, params = (route.name, route.is_returning, route.departure))

        data = {"route": route, "stops": list()}

        for row in cursor.fetchall():
            data["stops"].append((Entity.Stop(row[0], row[1]), row[2]))

        connection.close()

        self.master.load_new_page(RouteResults.RouteResults, data)


    def refresh(self):
        pass
