from Game import Game
from Players import Manual, AI
import time

def play(game, player1, player2, falsePositioning = False):
    game.showBoard(falsePositioning)
    
    letter = 'x'
    
    while game.winner == None:
        print("Player " + letter +"'s move")
        
        if letter == 'x':
            startTimeX = time.time()
            pos = player1.move(game)
            timeX = time.time() - startTimeX
        else:
            startTimeO = time.time()
            pos = player2.move(game)
            timeO = time.time() - startTimeO
            
        
        xstring = "Score for " + player1.letter +" is " + str(game.boardFitness(player1.letter)[0]) 
        xstring += "" if letter != 'x' else " Time : " + str(timeX)
        ostring = "Score for " + player2.letter +" is " + str(game.boardFitness(player2.letter)[0])
        ostring += "" if letter != 'o' else " Time : " + str(timeO)
        print(xstring)
        print(ostring)
        
        game.showBoard(falsePositioning)
        
        print(game.moves)
        letter = 'x' if letter == 'o' else 'o'

game = Game()
playerx = AI('x', longPro=True)
playero = AI('o', longPro=True)
#playero = Manual('o', longPro=True)
    
play(game, playerx, playero, falsePositioning = False)
#print(game.isInSquare((4,4)))
#try getpotentialmoves in 1 radius
#test counter_4 counter