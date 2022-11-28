from main import create_club

import server


class ClubMockResponse:

    @staticmethod
    def get_info():
        return {"name": "Club Test",
                "email": "example@gmail.com",
                "points": "20"}

    def __getitem__(self, item):
        return self.get_info()


def test_create_club(monkeypatch):
    def mock_get(*args, **kwargs):
        return ClubMockResponse()

    monkeypatch.setattr('main.Club', mock_get)

    expected_value = {"name": "Club Test",
                      "email": "example@gmail.com",
                      "points": "20"}
    assert create_club() == expected_value


def test_status_code_ok_index(client):
    response = client.get('/')
    assert response.status_code == 200


def test_should_handle_email_not_found(client, mocker):
    mocker.patch.object(server, 'clubs', [{"name": "Club Test",
                                           "email": "example@gmail.com",
                                           "points": "20"}])
    response = client.post('/show_summary',
                           data={"email": "leon.mark@outlook.com"},
                           follow_redirects=True)
    assert response.status_code == 400
    data = response.data.decode()
    assert data.find("Welcome to the GUDLFT Registration Portal!") == -1
