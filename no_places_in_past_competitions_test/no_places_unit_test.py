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
                "date": "2018-05-08 10:00:00",
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
                      "date": "2018-05-08 10:00:00",
                      "numberOfPlaces": "50"}
    assert create_competition() == expected_value


def test_status_code_ok_index(client):
    response = client.get('/')
    assert response.status_code == 200


def test_should_access_to_welcome_page(client, mocker):
    mocker.patch.object(server, 'clubs', [{"name": "Club Test",
                                           "email": "example@gmail.com",
                                           "points": "20"}])
    club = "example@gmail.com"
    response = client.post('/show_summary',
                           data={"email": club},
                           follow_redirects=True)
    assert response.status_code == 200
    data = response.data.decode()
    assert data.find("Welcome to the GUDLFT Registration Portal!") == -1


def _book_places_page(client, competition, club):
    response = client.get(f'/book/{competition}/{club}')

    assert competition == 'Competition Test'

    assert club == 'Club Test'

    assert response.status_code == 400


def test_should_not_be_able_to_book_places(client, mocker):
    mocker.patch.object(server, 'clubs', [{"name": "Club Test",
                                           "email": "example@gmail.com",
                                           "points": "20"}])
    mocker.patch.object(server, 'competitions', [{"name": "Competition Test",
                                                  "date": "2018-05-08 10:00:00",
                                                  "numberOfPlaces": "50"}])
    club = 'Club Test'
    competition = 'Competition Test'
    _book_places_page(client, competition, club)
