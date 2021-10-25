from mastrsql.utils import get_url, download_from_url


def test_get_url():
    assert type(get_url()) == str


