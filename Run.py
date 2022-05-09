from Game import Game
from Players import Manual, AI
import time

def play(game, player1, player2):
    game.showBoard()
    
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
            
        
        xstring = "Score for " + player1.letter +" is " + str(game.boardScore(player1.letter)) 
        xstring += "" if letter != 'x' else " Time : " + str(timeX)
        ostring = "Score for " + player2.letter +" is " + str(game.boardScore(player2.letter))
        ostring += "" if letter != 'o' else " Time : " + str(timeO)
        print(xstring)
        print(ostring)
        
        game.showBoard()
        
        print(game.moves)
        letter = 'x' if letter == 'o' else 'o'

game = Game()
playerx = AI('x')
playero = Manual('o')
    
play(game, playerx, playero)
#print(game.getDirection((7,7), (6,6)))
#add winner check
#add longpro variant to Manual
#add best move option if timer > 5 seconds
#add safeties to minimax for winner and tie(full board)