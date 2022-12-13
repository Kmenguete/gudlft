from gudlft import server


def test_should_not_access_to_points_boards(client, mocker):
    mocker.patch.object(server, 'clubs', [])
    club = None
    response = client.get('/points_board')
    assert club is None
    assert response.status_code == 401
