#from pyswip import Prolog
#prolog = Prolog()
#prolog.consult("C:\Users\Yap Xuan Ying\Documents\Prolog\Agent.pl")

'''
'#' => INDICATE WALL
'C' => INDICATE COIN
'A' => INDICATE AGENT
'W' => INDICATE WUMPUS
'P' => INDICATE CONFUNDUS PORTAL
' ' => INDICATE NOTHING/SAFE CELL
'''

Map = [ ['#', '#', '#' ,'#', '#', '#'],
        ['#', 'C', ' ' ,' ', 'P', '#'],
        ['#', 'P', ' ' ,' ', ' ', '#'],
        ['#', ' ', '#' ,'A', ' ', '#'],
        ['#', ' ', ' ' ,'P', ' ', '#'],
        ['#', 'W', ' ' ,' ', ' ', '#'],
        ['#', '#', '#' ,'#', '#', '#'] ]

# Agent's Knowledge/Estimate of each cell
def printAgentKB():
    Wall = False
    if Wall is True:
        print("# # #")
        print("# # #")
        print("# # #")
    else:
        confoundSignal = True
        stenchSignal = True
        tingleSignal = True
        NPCSignal = True
        guess = 'Wumpus'
        possibilities ={'Wumpus' : 'W',
                        'Portal' : 'O',
                        'rNorth' : '^',
                        'rEast' : '>',
                        'rSouth' : 'v',
                        'rWest' : '<',
                        'notVisitedSafe' : 's',
                        'visitedSafe' : 'S',
                        'Unknown' : '?'}
        
        glitterSignal = True
        bumpSignal = True
        ScreamSignal = True
        

        print("%", end=' ') if confoundSignal is True else print(".", end=' ')
        print("=", end=' ') if stenchSignal is True else print(".", end=' ')
        print("T", end=' ') if tingleSignal is True else print(".", end=' ')
        print()

        print("-", end=' ') if NPCSignal is True else print(" ", end=' ')
        print(possibilities.get(guess,"error"), end=' ')
        print("-", end=' ') if NPCSignal is True else print(" ", end=' ')
        print()

        print("*", end=' ') if glitterSignal is True else print(".", end=' ')
        print("B", end=' ') if bumpSignal is True else print(".", end=' ')
        print("@", end=' ') if ScreamSignal is True else print(".", end=' ')

printAgentKB()