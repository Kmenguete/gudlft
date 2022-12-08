from locust import HttpUser, task, between, SequentialTaskSet


CLUBS_CREDENTIALS = ["example@hotmail.com", "example2@hotmail.com", "example3@hotmail.com", "example4@hotmail.com",
                     "example5@hotmail.com", "example6@hotmail.com"]

COMPETITIONS = [{"name": "Competition Test",
                "date": "2023-06-09 10:00:00",
                "numberOfPlaces": "50"},
                {"name": "The Competition",
                "date": "2023-01-05 17:30:00",
                "numberOfPlaces": "90"}]


class ProjectPerformanceTest(HttpUser):
    @task
    class SequenceOfTasks(SequentialTaskSet):
        wait_time = between(1, 5)
        @task
        def index(self):
            self.client.get('/')
            self.client.get('http://127.0.0.1:5000/')

        @task
        def show_summary(self):
            self.client.options('http://127.0.0.1:5000/show_summary')
            self.client.post('http://127.0.0.1:5000/show_summary', json={"email": "example@hotmail.com"})

        @task
        def book(self):
            competition_name = "My competition"
            club_name = "The club test"
            self.client.options(f'http://127.0.0.1:5000/book/{competition_name}/{club_name}')
            self.client.get(f'http://127.0.0.1:5000/book/{competition_name}/{club_name}')


        @task
        def purchase_places(self):
            self.client.options('http://127.0.0.1:5000/purchase_places')
            self.client.post('http://127.0.0.1:5000/purchase_places', json={"club": "The club test",
                                                        "competition": "My competition",
                                                       "places": 6})
        @task
        def log_out(self):
            self.client.options('http://127.0.0.1:5000/logout')
            self.client.get('/logout')
