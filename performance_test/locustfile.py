from locust import HttpUser, task, between, SequentialTaskSet

CLUBS_CREDENTIALS = [{"name": "Club Test",
                      "email": "example@gmail.com",
                      "points": "20"},
                     {"name": "Club 2",
                      "email": "example2@gmail.com",
                      "points": "25"},
                     {"name": "Club 3",
                      "email": "example3@gmail.com",
                      "points": "30"},
                     {"name": "Club 4",
                      "email": "example4@gmail.com",
                      "points": "18"},
                     {"name": "Club 5",
                      "email": "example5@gmail.com",
                      "points": "15"},
                     {"name": "Club 6",
                      "email": "example6@gmail.com",
                      "points": "19"}]

COMPETITIONS = [{"name": "Competition Test",
                "date": "2023-06-09 10:00:00",
                "numberOfPlaces": "50"},
                {"name": "The Competition",
                "date": "2023-01-05 17:30:00",
                "numberOfPlaces": "90"}]


class User(HttpUser):

    @task
    class SequenceOfTask(SequentialTaskSet):
        wait_time = between(1, 5)
        club = "NOT FOUND"

        def on_start(self):
            if len(CLUBS_CREDENTIALS)> 0:
                self.club = CLUBS_CREDENTIALS.pop()
                self.client.options('http://127.0.0.1:5000/')
                self.client.get('http://127.0.0.1:5000/')

        @task
        def show_summary(self):
            self.client.options('http://127.0.0.1:5000/show_summary')
            self.client.post('http://127.0.0.1:5000/show_summary', json={"email": self.club['email']})

        @task
        def book(self):
            competition_name = COMPETITIONS[1]['name']
            club_name = self.club['name']
            self.client.options(f'http://127.0.0.1:5000/book/{competition_name}/{club_name}')
            self.client.get(f'http://127.0.0.1:5000/book/{competition_name}/{club_name}')

        @task
        def purchase_places(self):
            self.client.options('http://127.0.0.1:5000/purchase_places')
            self.client.post('http://127.0.0.1:5000/purchase_places', json={"club": self.club['name'],
                                                                            "competition": COMPETITIONS[1]['name'],
                                                                            "places": 6})

        def on_stop(self):
            self.client.options('http://127.0.0.1:5000/logout')
            self.client.get('http://127.0.0.1:5000/logout')
