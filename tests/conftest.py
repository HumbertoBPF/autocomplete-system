import mongomock
import pytest
from mongoengine import connect, disconnect

from app_factory import create_app
from database.models import Word, Meaning, Trie, WordCounter


@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    connect('dictionary', host='127.0.0.1', port=27017, mongo_client_class=mongomock.MongoClient)

    yield app

    disconnect()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def word(faker):
    word = Word(
        word=faker.word(),
        meanings=[
            Meaning(text=faker.text()),
            Meaning(text=faker.text()),
            Meaning(text=faker.text())
        ]
    )
    word.save()
    return word


@pytest.fixture
def trie():
    trie = Trie(
        prefix="ca",
        most_frequent_words=[
            WordCounter(word="car", counter=100),
            WordCounter(word="cat", counter=95),
            WordCounter(word="call", counter=90)
        ]
    )
    trie.save()
    return trie
