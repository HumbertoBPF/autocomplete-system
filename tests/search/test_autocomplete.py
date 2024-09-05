def test_autocomplete_no_result(client, trie):
    response = client.get("/autocomplete?query=ab")
    assert response.status_code == 200
    assert response.json == []


def test_autocomplete(client, trie):
    response = client.get("/autocomplete?query=ca")
    assert response.status_code == 200
    assert response.json == ["car", "cat", "call"]
