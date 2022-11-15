from main import create_club
from server import clubs


class ClubMockResponse:

    @staticmethod
    def get_info():
        return {"name": "Club Test",
                "email": "example@gmail.com",
                "points": "30"}


def test_create_club(monkeypatch):

    def mock_get(*args, **kwargs):
        return ClubMockResponse()

    monkeypatch.setattr('main.Club', mock_get)

    expected_value = {"name": "Club Test",
                      "email": "example@gmail.com",
                      "points": "30"}
    assert create_club() == expected_value


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


def test_should_access_to_points_boards(client):
    response = client.get('/points_board', data=[club for club in clubs], follow_redirects=True)
    assert response.status_code == 200
    data = response.data.decode()
    assert data.find("<ul><li>club['name']<br/>Points available: club['points]<li><ul>") == -1


def test_should_return_to_welcome_page(client):
    response = client.get('/back_to_welcome_page')
    assert response.status_code == 200


def test_should_logout(client):
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
