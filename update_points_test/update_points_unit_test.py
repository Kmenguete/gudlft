from main import create_club

from main import create_competition

import server


class ClubMockResponse:

    @staticmethod
    def get_info():
        return {"name": "Club Test",
                "email": "example@gmail.com",
                "points": "20"}

    def __getitem__(self, item):
        return self.get_info()


class CompetitionMockResponse:

    @staticmethod
    def get_info():
        return {"name": "Competition Test",
                "date": "2022-06-09 10:00:00",
                "numberOfPlaces": "50"}


def test_create_club(monkeypatch):
    def mock_get(*args, **kwargs):
        return ClubMockResponse()

    monkeypatch.setattr('main.Club', mock_get)

    expected_value = {"name": "Club Test",
                      "email": "example@gmail.com",
                      "points": "20"}
    assert create_club() == expected_value


def test_create_competition(monkeypatch):
    def mock_get(*args, **kwargs):
        return CompetitionMockResponse()

    monkeypatch.setattr('main.Competition', mock_get)

    expected_value = {"name": "Competition Test",
                      "date": "2022-06-09 10:00:00",
                      "numberOfPlaces": "50"}
    assert create_competition() == expected_value


def test_status_code_ok_index(client):
    response = client.get('/')
    assert response.status_code == 200


def test_should_access_to_welcome_page(client):
    email = "example@gmail.com"
    response = client.post('/show_summary',
                           data={"email": email},
                           follow_redirects=True)
    assert response.status_code == 200
    data = response.data.decode()
    assert data.find("Welcome to the GUDLFT Registration Portal!") == -1


def test_should_access_to_book_places_page(client):
    response = client.get('/book/<competition>/<club>')
    assert response.status_code == 200


def _purchase_places(client, club, competition, places):
    response = client.post('/purchase_places',
                           data={"club": club['name'],
                                 "competition": competition['name'],
                                 "places": places},
                           follow_redirects=True)
    assert response.status_code == 200
    data = response.data.decode()
    assert data.find("{{competition['name']}}") == -1


def test_should_update_points(client, mocker):
    clubs = mocker.patch.object(server, 'clubs', [{"name": "Club Test",
                                                   "email": "example@gmail.com",
                                                   "points": "20"}])
    competitions = mocker.patch.object(server, 'competitions', [{"name": "Competition Test",
                                                                 "date": "2022-06-09 10:00:00",
                                                                 "numberOfPlaces": "50"}])
    club = [club for club in clubs][0]
    competition = [competition for competition in competitions][0]
    _purchase_places(client, club, competition, 6)
    assert int(club['points']) == 14
