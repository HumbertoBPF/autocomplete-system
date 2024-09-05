from tests.utils import assert_word

url = "/search"


def test_search(client, word):
    response = client.get(f"{url}/{word.id}")
    assert response.status_code == 200
    assert_word(response.json, word)


def test_search_not_found(client, word):
    response = client.get(f"{url}/a{word.id}")
    assert response.status_code == 404
    assert response.json["error"] == "Not found"
