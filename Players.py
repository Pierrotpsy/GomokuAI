from math import inf
from random import randint

lines = {'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7, 'I':8, 'J':9, 'K':10, 'L':11, 'M':12, 'N':13, 'O':14}

class Manual():
    def __init__(self, letter, longPro = False):
        self.letter = letter
    
    def getValidPosition(self, t):
        while True:
            coord = 15 - (int(input("Enter " + t + " value between 1 and 15\n"))) if t == "row" else lines[(input("Enter " + t + " value between A and O\n"))]
            if(coord >= 0 and coord <= 14):
                return coord
            else:
                print("Choose positions between A1 and O15")
                
    def move(self, game):
        if(game.isBoardEmpty()):
            pos = (7, 7)
            game.playMove(pos, self.letter)
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
        
    def move(self, game):
        if(game.isBoardEmpty()):
            pos = (7, 7)
            game.playMove(pos, self.letter)
        elif(game.getNumPosLeft() == 223):
            x = randint(0,14)
            y = randint(0,14)
            while(game.isInSquare((x,y)) or not game.playMove((x,y), self.letter)):
                x = randint(0,14)
                y = randint(0,14)
        else:
            depth = 2
            check = self.minimax(game, depth, -inf, inf, True)
            if(game.playMove(check["coords"], self.letter)):
                return check["coords"]
    
    def minimax(self, game, depth, alpha, beta,isMax):
        maxP = self.letter
        minP = 'x' if self.letter == 'o' else 'o'
        
        if depth == 0:
            maxPlayerScore = 1*game.boardScore(maxP)
            minPlayerScore = -1*game.boardScore(minP)
            score = minPlayerScore + maxPlayerScore
            return {"score": score, "coords": None}
        
        if isMax:
            best = {"score":-inf, "coords":None}
            player = maxP
        else:
            best = {"score":inf, "coords": None}
            player = minP
        
        
        for pos in game.getNeighbours(potentialMoves = True):
            game.playMove(pos, player)
            check = self.minimax(game, depth-1, alpha, beta, not isMax)
            
            game.rollbackMove(pos, player)
            
            check["coords"] = pos
            if isMax:
                if check["score"] > best["score"]:
                    best = check
                alpha = max(alpha, check["score"])
                if beta <= alpha:
                    break
            else:
                if check["score"] < best["score"]:
                    best = check
                beta = min(beta, check["score"])
                if beta <= alpha:
                    break
        return best
                