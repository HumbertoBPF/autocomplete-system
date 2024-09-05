from mongoengine import disconnect

from database.config import connect_mongodb
from database.models import Word, Meaning

connect_mongodb()

meaning_1 = Meaning(
    text="a small, round container, often with a handle, used for drinking tea, coffee, etc., or the drink that it contains"
)
meaning_2 = Meaning(
    text="a specially designed cup, usually with two handles and often made of silver, given as a prize in a sports competition or a game or match in which the winner receives such a cup"
)
word = Word(word="cup", meanings=[meaning_1, meaning_2])
word.save()

disconnect()
