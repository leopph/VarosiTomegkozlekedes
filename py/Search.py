import ContentPage
import tkinter
import Entity
import mysql.connector
import RouteResults




class SearchResults(ContentPage.ContentPage):
    def __init__(self, data, *args, **kwargs):
        ContentPage.ContentPage.__init__(self, data, *args, **kwargs)

        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 9)

        title_frame = tkinter.Frame(master = self, bg = self["bg"])
        title_frame.grid(row = 0, sticky = "NESW")

        title_frame.rowconfigure(0, weight = 1)
        title_frame.columnconfigure(0, weight = 1)

        tkinter.Label(master = title_frame, text = data["from"].capitalize() + " - " + data["to"].capitalize(), font = (None, 24), bg = self["bg"]).grid(row = 0, column = 0, sticky = "NESW")
    

        result_frame = tkinter.Frame(master = self, bg = self["bg"])
        result_frame.grid(row = 1, sticky = "NESW")

        result_frame.columnconfigure(0, weight = 4)
        result_frame.columnconfigure(1, weight = 4)
        result_frame.columnconfigure(2, weight = 4)
        result_frame.columnconfigure(3, weight = 1)

        grid_row_count = 0
        for route_id, datalist in data["results"].items():
            for data in datalist:
                route = Entity.Route(route_id, data[0], data[3], data[1])

                tkinter.Label(result_frame, text = route.name, font = (None, 12), bg = "LightSkyBlue2").grid(row = grid_row_count, column = 0, sticky = "NESW")
                tkinter.Label(result_frame, text = route.type, font = (None, 12), bg = "LightSkyBlue2").grid(row = grid_row_count, column = 1, sticky = "NESW")
                tkinter.Label(result_frame, text = route.departure + data[2], font = (None, 12), bg = "LightSkyBlue2").grid(row = grid_row_count, column = 2, sticky = "NESW")
                tkinter.Button(result_frame, text = "Részletek", command = lambda route = route: self.route_details(route), bg = "dark slate blue", fg = "snow").grid(row = grid_row_count, column = 3, sticky = "NESW")

                grid_row_count += 1

    
    def route_details(self, route: Entity.Route):
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
