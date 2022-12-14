from gudlft import server


def test_book_places(client, mocker):
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
    club = clubs[0]
    competition = competitions[0]
    response_index = client.get("/")
    assert response_index.status_code == 200
    response_show_summary = client.post(
        "/show_summary", data={"email": club["email"]}, follow_redirects=True
    )
    assert response_show_summary.status_code == 200

    response_book = client.get(f'/book/{competition["name"]}/{club["name"]}')
    assert response_book.status_code == 200

    places = 6

    response_purchase_places = client.post(
        "/purchase_places",
        data={
            "club": club["name"],
            "competition": competition["name"],
            "places": places,
        },
        follow_redirects=True,
    )

    assert response_purchase_places.status_code == 200

    response_logout = client.get("/logout", follow_redirects=True)

    assert response_logout.status_code == 200
