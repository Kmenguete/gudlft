from gudlft.main import create_club


class ClubMockResponse:

    @staticmethod
    def get_info():
        return {"name": "Club Test",
                "email": "example@gmail.com",
                "points": "30"}


def test_create_club(mocker):

    mocker.patch('main.Club', return_value=ClubMockResponse())

    expected_value = {"name": "Club Test",
                      "email": "example@gmail.com",
                      "points": "30"}
    assert create_club() == expected_value
