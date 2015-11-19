#imports
import pickle
import json
import random
import os
import string
from trie import Trie
#funcoes: insert_key(k, v, trie), has_key(k, trie),
#retrieve_val(k, trie) e start_with_prefix(prefix, trie) 
#DB
#Array de cartas e de tries, ultimo index tem a trie de texto e o penúltimo tem a de nomes
from pprint import pprint
import re

#main
def main():
        global db
        global textTrie
        textTrie = [[]]
        db = []
        endFlag = 0
        print( "Start" )
        
#tests if db exists
        try:
                with open( 'AllCards.bin', "rb" ) as f:
                        db = pickle.load(f)
                        print( "Binary successfully loaded")
                        print(type(db))
                        print(db[0])    
        except:
                print( " binary not found" )            
                createDb()
        
        print( 'Welcome to the great Magic the Gathering DB' )
        
        while endFlag == 0:
                endFlag = printMenu()
                if endFlag == 0:
                        print('press any key')
                        c = input() #espera input pra mostrar o menu de novo

#prints the menu and asks for a command
def printMenu():
        os.system('cls') #limpa a tela / clear screen
        print( 'What are you looking for?' )
        print( '[0]Example \n[1]Search by name \n[2]Search by id \n\
[3]Search by prefix\n[4]Quit' )
        print( '>', end = "" )
        c = int(input());
        
#prints example ------- Working
        if c == 0:
                card = cardExample();
                printCard( card ) 
                return 0
                
#search by name ------- Needs implementation
        elif c == 1:
                print( 'And what is the name of the card?' )
                name = input();
                name = normalizeText(name)
                if has_key(name,nameTrie) == True: #ve se a carta ta no database
                        card = searchName( name ); 
                        printCard( card )
                else:
                        print('Card not in the database')
                return 0
                
#search by id
        elif c == 2:
                print( 'Please, insert card id' )
                ID = int(input())
                card = db[ID]
                pprint(card)
                return 0

#search by prefix
        elif c == 3:
                print( 'And what is the prefix you look for?' )
                prefix = input();
                prefix = normalizeText(prefix)
                namelist = start_with_prefix( prefix, nameTrie )
                for name in namelist:
                        card = searchName(name)
                        printCard (card)
                return 0
                
        elif c == 5:
                searchText( 'sword' )
                return 0
#ends process --------- Working
        elif c == 4:
                return 1 
        else:
                print( 'Please insert useful information' )
                
        
#creates db
def createDb():
        with open( 'AllCards.json' ) as data:
                jsondb = json.load( data );
                
        if jsondb:
                print( 'JSON database successfully loaded' )

#appends cards to db and creates its id
        i = 0
        for name,card in jsondb.items():
               db.append(jsondb[name])
               db[i]['id'] = i
               i +=1
        
#creates binary file
        with open('AllCards.bin','wb') as f:
            pickle.dump( db, f )
        
#creates a TRIE tree with the card names
        
        # nameTrie = [[]]
        textTrie = Trie()
        print(textTrie)
        # for i in range(0,len(db)):
        #         cardName = normalizeText(db[i]['name'])
        #         insert_key( cardName,i,nameTrie )
        # if nameTrie:
        #         print('Trie successfully created')
        #         #db.append(nameTrie)
        invertedListIndex = 0
        textList = []
        for i in range( 0, len( db )):
                print( i )
                tempWordList = []
                if( 'text' in db[ i ] ):
                        tempWordList = re.sub("[^\w]", " ",  db[ i ][ 'text' ]).split()
                if( len( tempWordList ) != 0 ):
                        for j in range( 0, len( tempWordList )):
                                tempWordList[ j ] =  tempWordList[ j ].lower()
                                if( textTrie.__contains__( tempWordList[ j ] ) ):
                                    index = textTrie.__getitem__( tempWordList[ j ])
                                    textList[ index ][ 'cards' ].append( i )
                                else:
                                    textTrie.__setitem__(tempWordList[ j ], invertedListIndex )
                                    obj = {}
                                    obj['word'] = tempWordList[ j ]
                                    obj['cards'] = []
                                    obj['cards'].append( i )
                                    textList.append( obj )
                                    invertedListIndex += 1

        index = textTrie.keys('love')
        print( index )
        obj = textList[ index ]
        print( obj )
        for i in range( 0, len(obj['cards'])):
        	printCard( db[obj['cards'][ i ]] )

                
                
        
#searchs for a card by name and returns it
def searchName(name):
        cardIndex = retrieve_val(name, nameTrie)
        return db[cardIndex]

#searchs for a card by name and returns it
def searchNameLinear(name):  
        for i in range(0,len(db)):
                if(normalizeText(db[i]['name']) == name()):
                        return( db[ i ] );
        return('Not found')

def searchText( word ):
        global textTrie 
        texTrie = [[]]
        insert_key( word, [0,1,2] , textTrie)
        array = (retrieve_val( word, textTrie))
        print(array)

        
#prints an example with random index
def cardExample():
        aCardIndex = random.randint(0,len(db))
        return db[aCardIndex]

#normaliza a string
def normalizeText(textoInicial):
        texto = textoInicial.strip()
        for pc in string.punctuation:
                texto = texto.replace(pc, '') #tira a pontuaçao do texto
        texto = texto.lower() #passa pra lowercase
        return texto

#prints all atributes of (card)
def printCard( card ):
                if ('name' in card) == True: 
                        print('Name: {}'.format(card['name']) )
                if ('id' in card) == True: 
                        print('ID: {}'.format(card['id']) )
                if ('layout' in card) == True:  
                        print('Layout: {}'.format(card['layout']) )
                if ('power' in card) == True:   
                        print('Power: {}'.format(card['power']) )
                if ('subtypes' in card) == True:        
                        print('Subtypes: {}'.format(card['subtypes']) )
                if ('type' in card) == True:    
                        print('Type: {}'.format(card['type']) )
                if ('types' in card) == True: 
                        print('Types: {}'.format(card['types']) )
                if ('colors' in card) == True:  
                        print('Colors: {}'.format(card['colors']) )
                if ('manaCost' in card) == True:        
                        print('Mana Cost: {}'.format(card['manaCost']) )
                if ('toughness' in card) == True:       
                        print('Toughness: {}'.format(card['toughness']) )
                if ('cmc' in card) == True:     
                        print('CMC: {}'.format(card['cmc']) )
                if ('text' in card) == True:    
                        print('Text: {}'.format(card['text']) ) 

#initFunctions
main();
