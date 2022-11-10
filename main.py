class Club:
    def __init__(self, name, email, points):
        self.name = name
        self.email = email
        self.points = points

    def get_info(self):
        info = {"name": self.name,
                "email": self.email,
                "points": self.points}
        return info


class Competition:
    def __init__(self, name, date, number_of_places):
        self.name = name
        self.date = date
        self.number_of_places = number_of_places

    def get_info(self):
        info = {"name": self.name,
                "date": self.date,
                "numberOfPlaces": self.number_of_places}
        return info


def create_club():
    club = Club("The mavericks", "andrea@mavericks.com", "17")
    info = club.get_info()
    return info


def create_competition():
    competition = Competition("Madrid Tournament", "2021-11-22 16:30:00", "29")
    info = competition.get_info()
    return info
