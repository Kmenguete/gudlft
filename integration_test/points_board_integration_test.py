import server


def test_book_places(client, mocker):
    clubs = mocker.patch.object(server, 'clubs', [{"name": "Club Test",
                                                   "email": "example@gmail.com",
                                                   "points": "20"}])

    club = clubs[0]

    response_index = client.get('/')
    assert response_index.status_code == 200
    response_show_summary = client.post('/show_summary',
                           data={"email": club["email"]},
                           follow_redirects=True)
    assert response_show_summary.status_code == 200

    response_get_points_of_clubs = client.get('/points_board')

    assert response_get_points_of_clubs.status_code == 200

    response_back_to_welcome_page = client.get('/back_to_welcome_page')

    assert response_back_to_welcome_page.status_code == 200

    response_logout = client.get('/logout', follow_redirects=True)

    assert response_logout.status_code == 200
