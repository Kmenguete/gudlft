from locust import HttpUser, task, between


club = {"name": "Club Test",
          "email": "example@gmail.com",
          "points": "20"}

competition = {"name": "Competition Test",
                "date": "2023-06-09 10:00:00",
                "numberOfPlaces": "500"}


class ProjectPerformanceTest(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        self.client.get('/')

    @task(3)
    def show_summary(self):
        self.client.post('/show_summary', {"email": club['email']})

    @task
    def book(self):
        competition_name = competition['name']
        club_name = club['name']
        self.client.get(f'/book/{competition_name}/{club_name}')


    @task
    def purchase_places(self):
        self.client.post('/purchase_places', {"club": club['name'],
                                                    "competition": competition['name'],
                                                   "places": 6})

    def on_stop(self):
        self.client.get('/logout')
