from mongoengine import connect


def connect_mongodb():
    connect('dictionary', host='127.0.0.1', port=27017)
