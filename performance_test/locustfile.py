from locust import Locust, TaskSet, task, between


club = {"name": "Club Test",
          "email": "example@gmail.com",
          "points": "20"}

competition = {"name": "Competition Test",
                "date": "2023-06-09 10:00:00",
                "numberOfPlaces": "500"}


class ProjectPerformanceTest(TaskSet):

    @task
    def index(self):
        self.client.get('/')

    @task
    def show_summary(self):
        self.client.post('/show_summary', json={"email": club['email']})

    @task
    def book(self):
        competition_name = competition['name']
        club_name = club['name']
        self.client.get(f'/book/{competition_name}/{club_name}')


    @task
    def purchase_places(self):
        self.client.post('/purchase_places', json={"club": club['name'],
                                                   "competition": competition['name'],
                                                   "places": 6})

    @task
    def logout(self):
        self.client.get('/logout')


class Club(Locust):
    task_set = ProjectPerformanceTest
    wait_time = between(5, 10)
