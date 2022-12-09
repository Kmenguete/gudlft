from locust import HttpUser, task, between, SequentialTaskSet


class User(HttpUser):

    @task
    class SequenceOfTask(SequentialTaskSet):
        wait_time = between(1, 5)

        def on_start(self):
            self.client.options('http://127.0.0.1:5000/')
            self.client.get('http://127.0.0.1:5000/')

        @task
        def show_summary(self):
            self.client.options('http://127.0.0.1:5000/show_summary')
            self.client.post('http://127.0.0.1:5000/show_summary', json={"email": "example@hotmail.com"})

        @task
        def book(self):
            competition_name = "Competition Test"
            club_name = "Club Test"
            self.client.options(f'http://127.0.0.1:5000/book/{competition_name}/{club_name}')
            self.client.get(f'http://127.0.0.1:5000/book/{competition_name}/{club_name}')

        @task
        def purchase_places(self):
            self.client.options('http://127.0.0.1:5000/purchase_places')
            self.client.post('http://127.0.0.1:5000/purchase_places', json={"club": "Club Test",
                                                                            "competition": "Competition Test",
                                                                            "places": 6})

        def on_stop(self):
            self.client.options('http://127.0.0.1:5000/logout')
            self.client.get('http://127.0.0.1:5000/logout')
