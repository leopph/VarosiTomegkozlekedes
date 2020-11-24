class User:
    def __init__(self, name: str, is_admin: bool):
        self._name = name
        self._is_admin = is_admin

    @property
    def name(self):
        return self._name

    @property
    def is_admin(self):
        return self._is_admin




class Route:
    def __init__(self, name: str, is_returning: bool, type: str, dep_time):
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
