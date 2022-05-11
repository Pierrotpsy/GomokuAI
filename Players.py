from math import inf
from random import randint
from threading import Timer
import operator

lines = {'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7, 'I':8, 'J':9, 'K':10, 'L':11, 'M':12, 'N':13, 'O':14}

class Manual():
    def __init__(self, letter, longPro = False):
        self.letter = letter
        self.longPro = longPro
    def getValidPosition(self, t):
        while True:
            coord = 15 - (int(input("Enter " + t + " value between 1 and 15\n"))) if t == "row" else lines[(input("Enter " + t + " value between A and O\n"))]
            if(coord >= 0 and coord <= 14):
                return coord
            else:
                print("Choose positions between A1 and O15")
                
    def move(self, game):
        if(game.isBoardEmpty() and self.longPro):
            pos = (7, 7)
            game.playMove(pos, self.letter)
        elif(game.getNumPosLeft() == 223 and self.longPro):
            colCoord = self.getValidPosition("column")
            rowCoord = self.getValidPosition("row")
            while(game.isInSquare((colCoord,rowCoord)) or not game.playMove((rowCoord,colCoord), self.letter)):
                colCoord = self.getValidPosition("column")
                rowCoord = self.getValidPosition("row")   
        else :
            while True:
                colCoord = self.getValidPosition("column")
                rowCoord = self.getValidPosition("row")
                
                if game.playMove((rowCoord, colCoord), self.letter):
                    return (rowCoord, colCoord)
                else:
                    print("Position is not valid, try again")
    
    
class AI():
    def __init__(self, letter, longPro = False):
        self.letter = letter
        self.longPro = longPro
        self.best = None
        self.overTime = False
          
    def stopLoop(self):
        self.overTime = True
        
    def move(self, game):
        if(game.isBoardEmpty() and self.longPro):
            pos = (7, 7)
            game.playMove(pos, self.letter)
        elif(game.getNumPosLeft() == 223 and self.longPro):
            x = randint(0,14)
            y = randint(0,14)
            while(game.isInSquare((x,y)) or not game.playMove((x,y), self.letter)):
                x = randint(0,14)
                y = randint(0,14)
        elif(game.boardFitness('x' if self.letter == 'o' else 'o')[1]["counter_4"] >= 1):
            print("autoblock")
            move, direction = game.autoBlock('x' if self.letter == 'o' else 'o')
            if(game.playMove(move, self.letter)):
                return move
            else:
                print("autobloc error, trying to correct")
                alternate = False
                newMove = tuple(map(operator.add, move, direction))
                if(game.playMove(newMove, self.letter)):
                    return newMove
                newMove = tuple(map(operator.sub, move, direction))
                if(game.playMove(newMove, self.letter)):
                    return newMove
                print("failed to correct error")
        else:
            self.overTime = False
            depth = 2
            t = Timer(4.95, self.stopLoop)
            t.start()
            check = self.minimax(game, depth, -inf, inf, True)
            if self.overTime:
                check = self.best
                #print("hey" + check)
            if(game.playMove(check["coords"], self.letter)):
                if self.overTime == False:
                    t.cancel()
                return check["coords"]
    
    def minimax(self, game, depth, alpha, beta,isMax):
        maxP = self.letter
        minP = 'x' if self.letter == 'o' else 'o'
        
        if(game.winner == True):
            return {"fitness": inf if isMax else -inf, "coords":None}
        
        if(game.isBoardFull()):
            return {"fitness": 0, "coords": None}
        
        if depth == 0:
            maxPlayerfitness = game.boardFitness(maxP)[0]
            minPlayerfitness = -1*game.boardFitness(minP)[0]
            fitness = minPlayerfitness + maxPlayerfitness
            return {"fitness": fitness, "coords": None}
        
        if isMax:
            best = {"fitness":-inf, "coords":None} 
            player = maxP
        else:
            best = {"fitness":inf, "coords": None}
            player = minP
        
        if(self.overTime):
            return
        
        for pos in game.getNeighbours(potentialMoves = True):
            game.playMove(pos, player)
            check = self.minimax(game, depth-1, alpha, beta, not isMax)
            
            game.rollbackMove(pos, player)
            if(self.overTime):
                return
            check["coords"] = pos
            if isMax:
                if check["fitness"] > best["fitness"]:
                    best = check
                    self.best = check
                alpha = max(alpha, check["fitness"])
                if beta <= alpha:
                    break
            else:
                if check["fitness"] < best["fitness"]:
                    best = check
                    self.best = check
                beta = min(beta, check["fitness"])
                if beta <= alpha:
                    break
        return best
                