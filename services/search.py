from flask import request
from mongoengine import ValidationError

from database.models import Word, Trie
from schemas import WordSchema
from utils.aws import log_to_cloudwatch
from utils.cors import MethodViewWithCors, cors


class SearchView(MethodViewWithCors):
    @cors
    def get(self):
        query_string = request.args

        query = query_string.get("query", "")

        try:
            word = Word.objects.get(word=query)
        except (Word.DoesNotExist, ValidationError):
            return {
                "error": "Not found"
            }, 404

        log_to_cloudwatch(word.word)

        schema = WordSchema()
        return schema.dump(word), 200


class AutocompleteView(MethodViewWithCors):
    @cors
    def get(self):
        query_string = request.args

        query = query_string.get("query", "")

        most_common_words = []
        trie = Trie.objects(prefix=query).first()

        if trie is not None:
            most_common_words = [word_counter.word for word_counter in trie.most_frequent_words]

        return most_common_words, 200
