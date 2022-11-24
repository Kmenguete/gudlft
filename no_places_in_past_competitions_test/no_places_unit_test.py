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


def test_should_access_to_welcome_page(client):
    email = "example@gmail.com"
    response = client.post('/show_summary',
                           data={"email": email},
                           follow_redirects=True)
    assert response.status_code == 200
    data = response.data.decode()
    assert data.find("Welcome to the GUDLFT Registration Portal!") == -1


def _book_places_page(client, competition, club):
    response = client.get('/book/<competition>/<club>',
                          data={"competition": competition,
                                "club": club},
                          follow_redirects=True)

    print("This is a competition in _book_places_page function: " + str(competition))
    print("***************************************************************************")
    print("This is a club in _book_places_page function: " + str(club))
    print("***************************************************************************")

    data = response.data.decode

    assert response.status_code == 302
    assert data.find('Book Places') == -1


def test_should_not_be_able_to_book_places(client, mocker):
    clubs = mocker.patch.object(server, 'clubs', [{"name": "Club Test",
                                                   "email": "example@gmail.com",
                                                   "points": "20"}])
    competitions = mocker.patch.object(server, 'competitions', [{"name": "Competition Test",
                                                                 "date": "2018-05-08 10:00:00",
                                                                 "numberOfPlaces": "50"}])
    club = clubs[0]
    competition = competitions[0]
    print("Here are clubs: " + str(clubs))
    print("***************************************************************************")
    print("Here are competitions: " + str(competitions))
    print("***************************************************************************")
    print("This is a club: " + str(club))
    print("***************************************************************************")
    print("This is a competition: " + str(competition))
    print("***************************************************************************")
    _book_places_page(client, competition, club)
