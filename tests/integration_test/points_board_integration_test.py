from gudlft import server


def test_book_places(client, mocker):
    clubs = mocker.patch.object(
        server,
        "clubs",
        [{"name": "Club Test", "email": "example@gmail.com", "points": "20"}],
    )

    club = clubs[0]

    response_index = client.get("/")
    assert response_index.status_code == 200
    response_show_summary = client.post(
        "/show_summary", data={"email": club["email"]}, follow_redirects=True
    )
    assert response_show_summary.status_code == 200

    club_name = "Club Test"

    response_get_points_of_clubs = client.get(f"/points_board/{club_name}")

    assert response_get_points_of_clubs.status_code == 200

    response_back_to_welcome_page = client.get(f"/back_to_welcome_page/{club_name}")

    assert response_back_to_welcome_page.status_code == 200

    response_logout = client.get("/logout", follow_redirects=True)

    assert response_logout.status_code == 200
