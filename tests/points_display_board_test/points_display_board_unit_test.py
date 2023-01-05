from gudlft import server


def test_status_code_ok_index(client):
    response = client.get("/")
    assert response.status_code == 200


def test_should_access_to_welcome_page(client, mocker):
    mocker.patch.object(
        server,
        "clubs",
        [{"name": "Club Test", "email": "example@gmail.com", "points": "20"}],
    )
    club = "example@gmail.com"
    response = client.post("/show_summary", data={"email": club}, follow_redirects=True)
    assert response.status_code == 200
    data = response.data.decode()
    assert data.find("Welcome to the GUDLFT Registration Portal!") == -1


def test_should_access_to_points_boards(client, mocker):
    clubs = mocker.patch.object(
        server,
        "clubs",
        [{"name": "Club Test", "email": "example@gmail.com", "points": "20"}],
    )
    club = clubs[0]["name"]
    response = client.get(f"/points_board/{club}", follow_redirects=True)
    assert club == "Club Test"
    assert response.status_code == 200
    data = response.data.decode()
    assert (
        data.find("<ul><li>club['name']<br/>Points available: club['points]<li><ul>")
        == -1
    )


def test_should_return_to_welcome_page(client, mocker):
    clubs = mocker.patch.object(
        server,
        "clubs",
        [{"name": "Club Test", "email": "example@gmail.com", "points": "20"}],
    )
    club_name = clubs[0]["name"]
    response = client.get(f"/back_to_welcome_page/{club_name}")
    assert response.status_code == 200


def test_should_logout(client):
    response = client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
