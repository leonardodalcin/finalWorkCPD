import json
from pprint import pprint

#inserts list of cards in db
db = [];
with open('magicCards.json') as data:
	db = json.load(data)
