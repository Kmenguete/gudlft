from locust import HttpUser, task, between


class ProjectPerformanceTest(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        self.client.get('/')

    @task
    def show_summary(self):
        self.client.post('/show_summary', json={"email": "example@hotmail.com"})

    @task
    def book(self):
        competition_name = "My competition"
        club_name = "The club test"
        self.client.get(f'/book/{competition_name}/{club_name}')


    @task
    def purchase_places(self):
        self.client.post('/purchase_places', json={"club": "The club test",
                                                    "competition": "My competition",
                                                   "places": 6})

    def on_stop(self):
        self.client.get('/logout')
