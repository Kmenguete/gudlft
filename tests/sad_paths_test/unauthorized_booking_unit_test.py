from gudlft import server


def _book_places_page(client, competition, club, number_of_places):
    response = client.get(f"/book/{competition}/{club}/{number_of_places}")

    assert competition == "Competition Test"

    assert club is None

    assert response.status_code == 401


def test_should_not_be_able_to_book_places(client, mocker):
    mocker.patch.object(server, "clubs", [])
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

    competition = "Competition Test"
    number_of_places = "50"
    _book_places_page(client, competition, club=None, number_of_places=number_of_places)
