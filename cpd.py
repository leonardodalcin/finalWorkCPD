#imports
import json
import random
import os
from pprint import pprint

def main():
	flagFIM = 0
	print("iniciou o programa")
	#ja existe database binaria?
	try: 
		with open('magicCards.bin','rb') as bindata:
			binario = bindata.read();
		print("achou o binario")
	except:
		#nao existe binario. criar novo
		print("nao achou o binario")            
		createDb() #le o .json, ordena, tira redundancias
	while flagFIM == 0:
		flagFIM = printMenu() #printa menu ate que retorne 1

#prints the menu and asks for a command
def printMenu():
	os.system('cls') #limpa a tela / clear screen
	print( 'Welcome to the great Magic the Gathering DB' )
	print( 'What are you looking for?' )
	print('[0]exemplo \n[1]search name \n[2]procura por ID \n[3]Fechar')
	c = int(input());
	if c == 0:
		#printa um exemplo de uma carta
		printCardExample();
		return 0 #main
	elif c == 1:
		#pesquisa uma carta pelo ['name']
		print( 'And what is the name of the beauty?' )
		name = input();
		searchName(name);       #precisara ser modificada pq
					#vai procurar direto no binario
		return 0 #main
	elif c == 2:
		print('Insira o ID da carta')
		ID = input()
		#searchID(ID) funcao a ser criada
		return 0 #main
	elif c == 3:
		# fim do while do main
		return 1 #flagFIM = 1 
	else:
		print( 'please insert useful information' )
	

def createDb():
	global db
	db = []
	with open( "AllCards.json") as data:
		jsondb = json.load( data );
	if jsondb:
		print('database .json loaded')

	i = 0
	for name,card in jsondb.items():
	       db.append(jsondb[name])
	       db[i]['id'] = i
	       i +=1
	
#search a card by name in the db and prints it
def searchName( name ):
        
	for i in range( 0, len( db )):
		if( db[ i ]['name'].lower() == name.lower()):
			pprint( db[ i ] );
			return

def printCardExample():
	#printa como exemplo uma carta de indice aleatorio
	aCardIndex = random.randint( 0, len(db))
	pprint(db[aCardIndex])

#initFunctions
main();
print('print depois do main')
