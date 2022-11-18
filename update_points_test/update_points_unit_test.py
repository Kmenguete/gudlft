from main import create_club

from main import create_competition


class ClubMockResponse:

    @staticmethod
    def get_info():
        return {"name": "Club Test",
                "email": "example@gmail.com",
                "points": "30"}

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
                      "points": "30"}
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


def test_should_update_points(client):
    club = ClubMockResponse.get_info()
    competition = CompetitionMockResponse.get_info()
    response = client.post('/purchase_places',
                           data={"club": club['name'],
                                 "competition": competition['name'],
                                 "places": 6},
                           follow_redirects=True)
    assert response.status_code == 200
    data = response.data.decode()
    assert data.find('How many places?') == -1
    expected_value = 24
    assert int(club['points']) == expected_value
