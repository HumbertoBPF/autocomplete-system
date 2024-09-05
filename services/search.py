from flask import request
from flask.views import MethodView
from mongoengine import ValidationError

from database.models import Word, Trie
from schemas import WordSchema
from utils.aws import log_to_cloudwatch


class SearchView(MethodView):
    def get(self, word_id):
        try:
            word = Word.objects.get(id=word_id)
        except (Word.DoesNotExist, ValidationError):
            return {
                "error": "Not found"
            }, 404

        log_to_cloudwatch(word.word)

        schema = WordSchema()
        return schema.dump(word), 200


class AutocompleteView(MethodView):
    def get(self):
        query_string = request.args

        query = query_string.get("query", "")

        most_common_words = []
        trie = Trie.objects(prefix=query).first()

        if trie is not None:
            most_common_words = [word_counter.word for word_counter in trie.most_frequent_words]

        return most_common_words, 200
