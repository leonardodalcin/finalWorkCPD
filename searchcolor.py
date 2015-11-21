#imports
import pickle
import json
import random
import os
import string
from trie import Trie
from pprint import pprint
import re
#cards[]-nameTrie-textTrie-textList
#main
def main():
        global db
        global textList
        global textTrie
        global nameTrie
        db = []
        endFlag = 0
        print( "Start" )
        
#tests if db exists
        try:
                with open( 'AllCards.bin', "rb" ) as f:
                        db = pickle.load(f)
                        print( "Binary successfully loaded")
                        textList = db.pop()
                        textTrie = db.pop()
                        nameTrie = db.pop()
        except:
                print( "Binary not found" )            
                createDb()
        
        print( '\nWelcome to the great Magic the Gathering DB' )
        
        while endFlag == 0:
                endFlag = printMenu()
                if endFlag == 0:
                        print('Press any key')
                        c = input('>') #espera input pra mostrar o menu de novo

#prints the menu and asks for a command
def printMenu():
        print( 'What are you looking for?' )
        print( '[0]Example \n[1]Search by name \n[2]Search by id \n[3]Text Search\n[4]Name prefix search\n[5]Text prefix search\n[6]Search by color\n[7]Quit' )
        print( '>', end = "" )
        c = int(input());
        
#prints example ------- Working
        if c == 0:
                card = cardExample();
                printCard( card ) 
                return 0
                
#search by name ------- Working
        elif c == 1:
                print( 'And what is the name of the card?' )
                name = input('>');
                name = normalizeText(name)
                if nameTrie.__contains__(name): #ve se a carta ta no database
                        card = searchName( name ); 
                        printCard( card )
                else:
                        print('Card not in the database')
                return 0
                
#search by id ------- Working
        elif c == 2:
                print( 'Please, insert card id' )
                ID = int(input('>'))
                card = db[ID]
                pprint(card)
                return 0

#search word in texts ------- Working
        elif c == 3:
                word = input('>');
                word = normalizeText( word )
                idsArray = searchText( word )
                for i in range( 0, len(idsArray)):
                        printCard(db[idsArray[i]])
                return 0
        
#serach by name prefix ------ Working
        elif c == 4:
                prefix = input();
                prefix = normalizeText( prefix )
                idsArray = searchNamePrefix( prefix )
                if idsArray:
                        for i in range( 0, len( idsArray )):
                                printCard( db[ idsArray[ i ]] )
                return 0
        
#serach by word prefix in text ------- Working
        elif c == 5:
                prefix = input();
                prefix = normalizeText( prefix )
                idsArray = searchTextPrefix( prefix )
                if idsArray:
                        for i in range( 0, len( idsArray )):
                                printCard( db[ idsArray[ i ]] )
                return 0
        elif c == 6:
                print( 'And what is the color of the card?' )
                print( 'Examples: Black  Blue  Green  Red  White')
                color = input('>')
                namecounter = 0 
                for i in range(0, len( db )):
                        if('colors' in db [ i ]):
                                if(namecounter < 20):  
                                        for j in range(0, len( db[ i ]['colors'])):
                                                if(db[ i ][ 'colors' ][ j ].lower() == color.lower()):
                                                        print(db [ i ][ 'name' ])
                                                        namecounter = namecounter + 1
                                else:
                                        print( '\nDo you wanna see more? Yes or No?' )
                                        a = input('>')
                                        if a.lower() == 'yes':
                                                namecounter = 0
                                        else:
                                                break
                                
                return 0
#ends process --------- Working
        elif c == 7:
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
         
#creates a TRIE tree with the words in cards texts
        textTrie = Trie()
        invertedListIndex = 0
        textList = []

        print('Generating Text Trie (this might take a while)')
        for i in range( 0, len( db )):
                tempWordList = []
                if( 'text' in db[ i ] ):
                        tempWordList = re.sub("[^\w]", " ",  db[ i ][ 'text' ]).split()
                if( len( tempWordList ) != 0 ):
                        for j in range( 0, len( tempWordList )):
                                tempWordList[ j ] =  tempWordList[ j ].lower()
                                if( textTrie.__contains__( tempWordList[ j ] ) ):
                                    index = textTrie.__getitem__( tempWordList[ j ])
                                    if i not in textList[index]['cards']:
                                            textList[ index ][ 'cards' ].append( i )
                                else:
                                    textTrie.__setitem__(tempWordList[ j ], invertedListIndex )
                                    obj = {}
                                    obj['word'] = tempWordList[ j ]
                                    obj['cards'] = []
                                    obj['cards'].append( i )
                                    textList.append( obj )
                                    invertedListIndex += 1
        print('Text Trie successfully created')
#creates a TRIE tree with the card names
        print('Generating Name Trie')
        nameTrie = Trie()
        for i in range(0, len(db)):
                cardName = normalizeText(db[i]['name'])
                if cardName:
                       nameTrie.__setitem__( cardName, i )
        print('Name Trie successfully created')
        print('Appending structures to db')
#appending our structures to db
        db.append(nameTrie)
        db.append(textTrie)
        db.append(textList)

#creates binary file
        print('Dumping binary file')
        with open('AllCards.bin','wb') as f:
            pickle.dump( db, f )
        print('Binary file successfully created')

#searchs for a text and returns indexes array
def searchText( word ):     
        index = textTrie.__getitem__( word )
        array = textList[ index ]
        return( array['cards'] )

#searchs text prefix
def searchTextPrefix( prefix ):
        indexes = []
        idsArray = []
        wordsArray = textTrie.__keys__( prefix )
        if len( wordsArray ) != 0:
                if len( wordsArray ) == 1:
                        return 0
                del wordsArray[0]
                for i in range(0, len( wordsArray )):
                        indexes.append( textTrie.__getitem__( wordsArray[ i ] ))
                for i in range(0, len( indexes )):
                        for j in range(0, len( textList[ indexes[ i ]][ 'cards' ] )):
                                idsArray.append( textList[ indexes[ i ]][ 'cards' ][ j ] )
                return idsArray
        else:
                return 0
        
#searchs name prefix
def searchNamePrefix( prefix ):
        indexes = []
        idsArray = []
        wordsArray = nameTrie.__keys__( prefix )
        if len( wordsArray ) != 0:
                if len( wordsArray ) == 1:
                        return 0
                del wordsArray[0]
                for i in range(0, len( wordsArray )):
                        indexes.append( nameTrie.__getitem__( wordsArray[ i ] ))
                return indexes
        else:
                return 0
        
        
#searchs for a card by name and returns it
def searchName(name):
        cardIndex = nameTrie.__getitem__( name )
        return db[cardIndex]
        
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