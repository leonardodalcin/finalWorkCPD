#imports
import json
import random
from pprint import pprint

def main():
#inserts list of cards in db
	printMenu();
#prints the menu and asks for a command
def printMenu():
	print( 'Welcome to the great Magic the Gathering DB' )
	print( 'What are you looking for?' )
	print('[0]card Example [1]search Name' )
#gets desired user action, converting it to integer
	c = int(input());
	print(c);
	if c == 0:
		printCardExample();
		main();
	elif c == 1:
		print( 'And what is the name of the beauty?' )
		name = input();
		searchName(name);
		main();
	else:
		print( 'please insert useful information' )
		main();

#creates the db
def createDb():
#db is now a global variable
	global db
	db = [];
	with open( 'magicCards.json' ) as data:
		db = json.load( data );

#search a card by name in the db and prints it
def searchName( name ):
	for i in range( 0, len( db )):
		if( db[ i ][ 'name' ] == name ):
			pprint( db[ i ] );

def printCardExample():
	aCardIndex = random.randint( 0, len( db ))
	pprint( db[ aCardIndex ] )
#initFunctions
createDb();
main();
