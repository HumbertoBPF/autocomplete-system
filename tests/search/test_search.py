from tests.utils import assert_word

url = "/search"


def test_search(client, word):
    response = client.get(f"{url}?query={word.word}")
    assert response.status_code == 200
    assert_word(response.json, word)


def test_search_not_found(client, word):
    response = client.get(f"{url}?query=a{word.word}")
    assert response.status_code == 404
    assert response.json["error"] == "Not found"
