from flask import Flask

from services.search import AutocompleteView, SearchView


def create_app():
    app = Flask(__name__)

    app.add_url_rule("/search", view_func=SearchView.as_view("search"))
    app.add_url_rule("/autocomplete", view_func=AutocompleteView.as_view("autocomplete"))

    return app
