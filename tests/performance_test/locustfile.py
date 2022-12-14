import json
import random

from locust import HttpUser, task, between, SequentialTaskSet


def load_clubs():
    with open("/gudlft/clubs.json") as c:
        list_of_clubs = json.load(c)["clubs"]
        return list_of_clubs


def load_competitions():
    with open("/gudlft/competitions.json") as comps:
        list_of_competitions = json.load(comps)["competitions"]
        return list_of_competitions


clubs = load_clubs()

competitions = load_competitions()


class User(HttpUser):
    @task
    class SequenceOfTask(SequentialTaskSet):
        wait_time = between(1, 5)

        def on_start(self):
            self.client.options("http://127.0.0.1:5000/")
            self.client.get("http://127.0.0.1:5000/")

        @task
        def show_summary(self):
            club = random.choice(clubs)
            self.client.options("http://127.0.0.1:5000/show_summary")
            self.client.post(
                "http://127.0.0.1:5000/show_summary", {"email": club["email"]}
            )

        @task
        def book(self):
            club = random.choice(clubs)
            competition = random.choice(competitions)
            competition_name = competition["name"]
            club_name = club["name"]
            self.client.options(
                f"http://127.0.0.1:5000/book/{competition_name}/{club_name}"
            )
            self.client.get(
                f"http://127.0.0.1:5000/book/{competition_name}/{club_name}"
            )

        @task
        def purchase_places(self):
            club = random.choice(clubs)
            competition = random.choice(competitions)
            self.client.options("http://127.0.0.1:5000/purchase_places")
            self.client.post(
                "http://127.0.0.1:5000/purchase_places",
                {"club": club["name"], "competition": competition["name"], "places": 6},
            )

        def on_stop(self):
            self.client.options("http://127.0.0.1:5000/logout")
            self.client.get("http://127.0.0.1:5000/logout")
