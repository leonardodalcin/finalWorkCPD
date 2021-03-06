#Imports
import pickle
import json
import random
import string
from trie import Trie
from pprint import pprint
import re

##ordem dos dados no binario:
## db[0:n-3] == cards[]
## db[n-2] == nameTrie
## db[n-1] == textTrie
## db[n] == textList

def main():
        global db
        global textList
        global textTrie
        global nameTrie
        global dbcolor
        db = []
        dbcolor = {}
        endFlag = 0
        print( "Start" )
        
#Tests if DB exists
        try:
                with open( 'AllCards.bin', "rb" ) as f:
                        db = pickle.load(f)
                        print( "Binary successfully loaded")
                        dbcolor = db.pop()
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
                        c = input('>')
                        
#Prints the menu and asks for a command
def printMenu():
        print( 'What are you looking for?' )
        print( '[0]Example \n[1]Search by name \n[2]Search by id')
        print('[3]Text Search\n[4]Name prefix search\n[5]Search by color')
        print('[6]Search by mana cost\n[7]Quit')
        print( '>', end = "" )
        try: #se input nao for um int, 'Please insert useful information'
            c = int(input());
        
    #Prints example
            if c == 0:
                    card = cardExample();
                    printCard( card ) 
                    return 0
                    
    #Search by name
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
                    
    #Search by id
            elif c == 2:
                print( 'Please, insert card id' )
                ID = input()
                try:
                    if int(ID) in range(0,len(db)):
                        ID = int(ID)
                        card = db[ID]
                        printCard(card)
                    else:
                        print('Invalid ID')
                except:
                    print('Invalid ID') #caso o input nao seja um int
                return 0

    #Search word in texts
            elif c == 3:
                print('Insert a word from a card\'s text')
                word = input();
                word = normalizeText( word )
                if textTrie.__contains__(word):
                    idsArray = searchText( word )
                    printCardArray(idsArray)
                else:
                    print('This word doesn\'t appear in any card text')
                return 0
            
    #Search by name prefix
            elif c == 4:
                print('Insert a prefix of a card\'s name')
                prefix = input();
                prefix = normalizeText( prefix )
                idsArray = searchNamePrefix( prefix )
                if idsArray:
                    printCardArray(idsArray)
                else:
                    print('Nothing found.')
                return 0

    #Search by color 
            elif c == 5:
                    searchColor()            
                    return 0
    #Search by mana cost
            elif c == 6:
                    flag = searchManaCost()
                    if(flag == 0):
                            print( 'There is no cards with this mana cost, sorry.' )
                    return 0
                                    
    #Ends process 
            elif c == 7:
                    return 1 
            else:
                    print( 'Please insert useful information' )
                    return 0
        except:
            print( 'Please insert useful information' )
            return 0


#Creates Database
def createDb():

    global textList
    global textTrie
    global nameTrie

    with open( 'AllCards.json' ) as data:
        jsondb = json.load( data );
    if jsondb:
        print( 'JSON database successfully loaded' )

#Appends cards to db and creates its id
    i = 0
    for name,card in jsondb.items():
       db.append(jsondb[name])
       db[i]['id'] = i
       i +=1
               
#Creates a TRIE tree with the words in cards texts
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
        
#Calling the ColorIndexing()
    colorIndexing()
        
#Creates a TRIE tree with the card names
    print('Generating Name Trie')
    nameTrie = Trie()
    for i in range(0, len(db)):
        cardName = normalizeText(db[i]['name'])
        if cardName:
           nameTrie.__setitem__( cardName, i )
    print('Name Trie successfully created')
    print('Appending structures to db')
        
#Appending our structures to db
    db.append(nameTrie)
    db.append(textTrie)
    db.append(textList)
    db.append(dbcolor)
        
#Creates binary file
    print('Dumping binary file')
    with open('AllCards.bin','wb') as f:
        pickle.dump( db, f )
    print('Binary file successfully created')
        
#Creates a color inverted index
#retorna 0
def colorIndexing():
    global dbcolor
    dbcolor['black'] = []
    dbcolor['blue'] = []
    dbcolor['white'] = []
    dbcolor['green'] = []
    dbcolor['red'] = []
    for i in range(0, len( db )):
        if('colors' in db [ i ]):
            for j in range(0, len( db[ i ]['colors'])):     
                if(db[ i ][ 'colors' ][ j ] == 'Black'):
                    dbcolor['black'].append( i )
                elif(db[ i ][ 'colors' ][ j ] == 'Green'):
                    dbcolor['green'].append( i )
                elif(db[ i ][ 'colors' ][ j ] == 'Blue'):
                    dbcolor['blue'].append( i )
                elif(db[ i ][ 'colors' ][ j ] == 'White'):
                    dbcolor['white'].append( i )
                elif(db[ i ][ 'colors' ][ j ] == 'Red'):
                    dbcolor['red'].append( i )
    print( 'Color index successfully loaded' )
    return 0

#Search for a text and returns indexes array
#retorna uma lista de indices de cartas que estao na textList
def searchText( word ):     
    index = textTrie.__getitem__( word )
    array = textList[ index ]
    return( array['cards'] )
        
#Search by name prefix
#retorna uma lista de indices de cartas que estao na textList
def searchNamePrefix(prefix):
    global nameTrie
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

#retorna 0 caso nao tenha encontrado nada
def searchManaCost():
    print( 'This is the search by mana cost' )
    print( 'Examples:')
    print( '{B} Black {U} Blue {W} White {R} Red {G} Green' )
    print( '{X} Undefined colors of mana  X = 1,2,3,4,...' )
    print( '{G/W} Can use one green mana or one white mana' )
    print( '{X/U} X Undefined colors of mana or one blue mana' )
    print( 'Example:' )
    card = cardExample()
    print( 'Name: {}'.format( card['name'] ) )
    if 'manaCost' in card:
        print( 'Mana Cost: {}'.format( card['manaCost'] ) )
    else:
        print( 'This card doesnt need mana' )
    print( 'And what is the mana cost of the card?' )
    manacost = input('>')
    counter = 0
    flag = 0
    for i in range( 0, len(db)):
        if(counter < 20):
            if ('manaCost' in db[ i ]) == True:
                if db[ i ]['manaCost'] == manacost:
                    print(db[ i ]['name'] + ' ID:{}'.format(db[ i ]['id']))
                    counter += 1
                    flag = 1
        else:
            print( 'Do you wanna see more? Yes or No?' )
            a = input('>')
            if a.lower() == 'yes':
                counter = 0
            if a.lower() == 'no':
                break
    return flag

#printa todas as cartas de certa cor
def searchColor():
    print( 'And what is the color of the card?' )
    print( 'Examples: Black  Blue  Green  Red  White')
    color = input('>')
    color = normalizeText(color)
    printCardArray(dbcolor[color])

#a partir de uma lista de indices, printa as cartas desses indices
def printCardArray(cardIndexesArray):
    arrayLenght = len(cardIndexesArray)
    if arrayLenght > 5:
        printcounter = 0
        for i in range( 0, arrayLenght ):
            if(printcounter < 20): #printa 20 de cada vez
                print(db[cardIndexesArray[i]]['name'] + ' ID:{}'.format(db[cardIndexesArray[i]]['id']))
                printcounter += 1
            else:
                print( 'Do you wanna see more? Yes or No?' )
                a = input('>')
                if a.lower() == 'yes':
                    printcounter = 0 #printa mais 20
                if a.lower() == 'no':
                    break
    else:
        for i in range(0,arrayLenght):
            print(db[cardIndexesArray[i]]['name'] + ' ID:{}'.format(db[cardIndexesArray[i]]['id']))
        
#Search for a card by name and returns it
#retorna uma carta
def searchName(name):
    cardIndex = nameTrie.__getitem__( name )
    return db[cardIndex]
        
#retorna uma carta
def cardExample():
    aCardIndex = random.randint(0,len(db))
    return db[aCardIndex]

#Normaliza uma string
def normalizeText(textoInicial):
    texto = textoInicial.strip()
    for pc in string.punctuation:
        texto = texto.replace(pc, '')
    texto = texto.lower() 
    return texto

#Prints all atributes of a card
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
                        
#InitFunctions
main();
