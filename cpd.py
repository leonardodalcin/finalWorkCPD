#imports
import json
import random
import os
import re
from pprint import pprint

#main
def main():
	endFlag = 0
	print( "Start" )
	
#tests if db exists
	try: 
		with open( 'magicCards.bin', 'rb' ) as bindata:
			bin = bindata.read();
		print( "Binary successfully loaded" )
		
	except:
		print( "Opss, binary not found" )            
		createDb()
	
	print( 'Welcome to the great Magic the Gathering DB' )
	
	while endFlag == 0:
		endFlag = printMenu()

#prints the menu and asks for a command
def printMenu():
	print( 'What are you looking for?' )
	print( '[0]Example \n[1]Search by name \n[2]Search by id \n[3]Quit' )
	print( '>', end = "" )
	c = int(input());
	
#prints example ------- Working
	if c == 0:
		card = cardExample();
		pprint( card ) 
		return 0
		
#search by name	------- Needs implementation
	elif c == 1:
		print( 'And what is the name of the beauty?' )
		name = input();
		card = searchName( name ); 
		pprint( card )
		return 0
		
#search by id -------- Needs a B-tree
	elif c == 2:
		print( 'Please, insert card id' )
		ID = input()
		return 0
		
#ends process --------- Working
	elif c == 3:
		return 1
		
	else:
		print( 'Please insert useful information' )
	
#creates db
def createDb():
	global db
	db = []
	
	with open( "magicCards.json" ) as data:
		jsondb = json.load( data );
		
	if jsondb:
		print( 'JSON database successfully loaded' )

#appends cards to db and creates its id
	i = 0
	for name,card in jsondb.items():
	       db.append( jsondb[ name ])
	       db[ i ][ 'id' ] = i
	       i = i + 1
		   
	createTextTrie()
	
def createTextTrie():
	wordList = []
	for i in range( 0, len( db )):
		wordList = re.sub("[^\w]", " ",  db[ i ][ text ]).split()
		print( wordList )
	
#searchs for a card by name and returns it
def searchName( name ):  
	for i in range( 0, len( db )):
		if( db[ i ][ 'name' ].lower() == name.lower()):
			return( db[ i ] );
	
	return( 'Not found' )
	
#prints an example with random index
def cardExample():
	aCardIndex = random.randint( 0, len( db ))
	return( db[ aCardIndex ])

#initFunctions
main();
