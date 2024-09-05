from mongoengine import Document, StringField, ListField, EmbeddedDocument, EmbeddedDocumentField, IntField


class Meaning(EmbeddedDocument):
    text = StringField(required=True)


class WordCounter(EmbeddedDocument):
    word = StringField(required=True)
    counter = IntField(required=True)


class Word(Document):
    word = StringField(required=True)
    meanings = ListField(EmbeddedDocumentField(Meaning))


class Trie(Document):
    prefix = StringField(required=True, unique=True)
    most_frequent_words = ListField(EmbeddedDocumentField(WordCounter))
