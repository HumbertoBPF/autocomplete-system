from database.models import Word


def assert_word(word_json, word: Word):
    meanings_json = word_json["meanings"]

    assert word_json["word"] == word.word
    assert meanings_json[0]["text"] == word.meanings[0].text
    assert meanings_json[1]["text"] == word.meanings[1].text
    assert meanings_json[2]["text"] == word.meanings[2].text
