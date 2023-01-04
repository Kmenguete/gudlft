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


def _should_find_competition_and_club(client, competition, club, number_of_places):
    response = client.get(f"/book/{competition}/{club}/{number_of_places}")
    assert competition == "Competition Test"
    assert club == "Club Test"
    assert response.status_code == 200


def test_should_access_to_book_places_page(client, mocker):
    mocker.patch.object(
        server,
        "clubs",
        [{"name": "Club Test", "email": "example@gmail.com", "points": "20"}],
    )
    mocker.patch.object(
        server,
        "competitions",
        [
            {
                "name": "Competition Test",
                "date": "2023-06-09 10:00:00",
                "numberOfPlaces": "50",
            }
        ],
    )
    club = "Club Test"
    competition = "Competition Test"
    number_of_places = "50"
    _should_find_competition_and_club(client, competition, club, number_of_places)


def _purchase_places(client, club, competition, places):
    response = client.post(
        "/purchase_places",
        data={
            "club": club["name"],
            "competition": competition["name"],
            "places": places,
        },
        follow_redirects=True,
    )
    assert response.status_code == 400
    data = response.data.decode()
    assert data.find("{{competition['name']}}") == -1


def test_should_not_book_more_than_12_places(client, mocker):
    clubs = mocker.patch.object(
        server,
        "clubs",
        [{"name": "Club Test", "email": "example@gmail.com", "points": "20"}],
    )
    competitions = mocker.patch.object(
        server,
        "competitions",
        [
            {
                "name": "Competition Test",
                "date": "2023-06-09 10:00:00",
                "numberOfPlaces": "50",
            }
        ],
    )
    club = [club for club in clubs][0]
    competition = [competition for competition in competitions][0]
    _purchase_places(client, club, competition, 16)
