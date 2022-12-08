from locust import HttpUser, task, between, TaskSet


CLUBS_CREDENTIALS = ["example@hotmail.com", "example2@hotmail.com", "example3@hotmail.com", "example4@hotmail.com",
                     "example5@hotmail.com", "example6@hotmail.com"]

COMPETITIONS = [{"name": "Competition Test",
                "date": "2023-06-09 10:00:00",
                "numberOfPlaces": "50"},
                {"name": "The Competition",
                "date": "2023-01-05 17:30:00",
                "numberOfPlaces": "90"}]


class ProjectPerformanceTest(TaskSet):
    @task
    class SequenceOfTasks(HttpUser):
        wait_time = between(1, 5)

        club = "NOT FOUND"


        def on_start(self):
            if len(CLUBS_CREDENTIALS) > 0:
                self.club = CLUBS_CREDENTIALS.pop()
                self.client.options('http://127.0.0.1:5000/')
                self.client.get('http://127.0.0.1:5000/')

        @task
        def show_summary(self):
            self.client.options('http://127.0.0.1:5000/show_summary')
            self.client.post('http://127.0.0.1:5000/show_summary', json={"email": "example@hotmail.com"})

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
