from gudlft import server


def test_should_not_access_to_welcome_page(client, mocker):
    mocker.patch.object(server, 'clubs', [])
    club = None
    response = client.get('/back_to_welcome_page')
    assert club is None
    assert response.status_code == 401
