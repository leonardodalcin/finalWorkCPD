##imports
import pickle
import json
import random
import os
import string
from trie import *
from pprint import pprint
import re

##ordem dos dados no binario:
## db[0:n-3] == cards[]
## db[n-2] == nameTrie
## db[n-1] == textTrie
## db[n] == textList

#main
def main():
    global db
    global textList
    global textTrie
    global nameTrie
    db = []
    endFlag = 0
    print( "Start" )

    ##tests if db exists
    try:
        with open( 'AllCards.bin', "rb" ) as f:
            db = pickle.load(f)
        print( "Binary successfully loaded")
        textList = db.pop()
        textTrie = db.pop()
        nameTrie = db.pop()
    except:
        print( "Binary not found")
        createDb()

    print( 'Welcome to the great Magic the Gathering DB')

    while endFlag == 0:
        endFlag = printMenu()
        if endFlag == 0:
            print('press any key')
            c = input() #espera input pra mostrar o menu de novo

##prints the menu and asks for a command
#retorna 0 ou 1 
def printMenu():
    print( 'What are you looking for?')
    print( '[0]Example \n[1]Search by name \n[2]Search by id')
    print('[3]Text Search\n[4]Name prefix search\n[5]Quit')
    print( '>', end = "" )
    c = int(input());

    ##prints example ------- Working
    if c == 0:
        card = cardExample();
        printCard( card ) 
        return 0

    ##search by name ------- Working
    elif c == 1:
        print( 'And what is the name of the card?')
        name = input();
        name = normalizeText(name)
        if nameTrie.__contains__(name): #ve se a carta ta no database
            card = searchName( name ); 
            printCard( card )
        else:
            print('Card not in the database')
        return 0

    ##search by id ------- Working
    elif c == 2:
        print( 'Please, insert card id' )
        ID = int(input())
        if ID in range(0,len(db)):
            card = db[ID]
            printCard(card)
        else:
            print('Invalid ID')
        return 0

    ##search word in texts ------- Working
    elif c == 3:
        print('Insert a word from a card\'s text')
        word = input();
        word = normalizeText( word )
        if textTrie.__contains__(word):
            idsArray = searchText( word )
            for i in range( 0, len(idsArray)):
                printCard(db[idsArray[i]])
        else:
            print('This word doesn\'t appear in any card text')
        return 0

    ##serach by name prefix ------ Working
    elif c == 4:
        print('Insert a prefix of a card\'s name')
        prefix = input();
        prefix = normalizeText( prefix )
        idsArray = searchNamePrefix( prefix )
        if idsArray:
            for i in range( 0, len( idsArray )):
                printCard( db[ idsArray[ i ]] )
        else:
            print('Nothing found.')
        return 0

##ends process --------- Working
    elif c == 5:
        return 1 
    else:
        print( 'Please insert useful information' )


##creates db
#nao retorna nada
def createDb():
    with open( 'AllCards.json' ) as data:
        jsondb = json.load( data );

    if jsondb:
        print( 'JSON database successfully loaded' )

    ##appends cards to db and creates its id
    i = 0
    for name,card in jsondb.items():
        db.append(jsondb[name])
        db[i]['id'] = i
        i +=1

    ##creates a TRIE tree with the words in cards texts
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
    ##creates a TRIE tree with the card names
    print('Generating Name Trie')
    nameTrie = Trie()
    for i in range(0, len(db)):
            cardName = normalizeText(db[i]['name'])
            if cardName:
                    nameTrie.__setitem__( cardName, i )
    print('Name Trie successfully created')
    print('Appending structures to db')
    ##appending our structures to db
    #os 3 ultimos elementos de db[] serão ocupados por outras estruturas de dados
    db.append(nameTrie) 
    db.append(textTrie)
    db.append(textList)

    ##creates binary file
    print('Dumping binary file')
    with open('AllCards.bin','wb') as f:
            pickle.dump( db, f )
    print('Binary file successfully created')

##searchs for a text and returns indexes array
#retorna uma lista de indices de cartas que estao na textList
def searchText( word ):     
    index = textTrie.__getitem__( word )
    array = textList[ index ]
    return( array['cards'] )

##searchs text prefix
#retorna uma lista de indices de cartas que estao na textList
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

##searchs name prefix
#retorna uma lista de indices de cartas que estao na textList
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


##searchs for a card by name and returns it
#retorna uma carta
def searchName(name):
    cardIndex = nameTrie.__getitem__( name )
    return db[cardIndex]

#retorna uma carta aleatoria
def cardExample():
    aCardIndex = random.randint(0,len(db))
    return db[aCardIndex]

##normaliza a string
#retorna uma string
def normalizeText(textoInicial):
    texto = textoInicial.strip()
    for pc in string.punctuation:
        texto = texto.replace(pc, '') #tira a pontuaçao do texto
    texto = texto.lower() #passa pra lowercase
    return texto

##prints all atributes of (card)
#nao retorna nada
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

##initFunctions
main();
