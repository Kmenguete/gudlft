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


def _book_places_page(client, competition, club, number_of_places):
    response = client.get(f"/book/{competition}/{club}/{number_of_places}")

    assert competition == "Competition Test"

    assert club == "Club Test"

    assert response.status_code == 400


def test_should_not_be_able_to_book_places(client, mocker):
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
                "date": "2018-05-08 10:00:00",
                "numberOfPlaces": "50",
            }
        ],
    )
    club = "Club Test"
    competition = "Competition Test"
    number_of_places = "50"
    _book_places_page(client, competition, club, number_of_places)
