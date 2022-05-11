import math
import operator


LINES = {'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7, 'I':8, 'J':9, 'K':10, 'L':11, 'M':12, 'N':13, 'O':14}
MOVE_VALUES = {"counter_2": 1, "open_2": 2, "counter_3": 5, "open_3": 20, "counter_4": 200, "open_4": 2000, "win": 20000}


class Game():
    def __init__(self):
        self.board = self.newBoard()
        self.moves = {'x':[], 'o':[]}  
        self.winner = None
        
    def newBoard(self):
        board = [['-' for _ in range(15)] for _ in range(15)]
        return board
    
    def showBoard(self):
        for i in range(15):
            nums = str(15-i) 
            nums  = nums.rjust(3)
            print(nums + '| ' + ' | '.join(self.board[i]) + ' |')
        
        s = "  "
        for i in range(15):
            s += (" | " + list(LINES.keys())[i])
        s += " |"
        print(s)
        
    def playMove(self, move, char):
        if(self.board[move[0]][move[1]] == '-'):
            self.moves[char].append(move)
            self.board[move[0]][move[1]] = char
            if self.boardFitness(char)[0] >= MOVE_VALUES["win"]:
                self.winner = char
            return True
        else:
            return False
        
    def rollbackMove(self, move, char):
        if(self.board[move[0]][move[1]] == char):
            self.moves[char].remove(move)
            self.board[move[0]][move[1]] = '-'
            if self.winner != None:
                self.winner = None
            return True
        else:
            return False
    
    def isBoardEmpty(self):
        return len(self.moves['x']) == 0 and len(self.moves['o']) == 0
    
    # checks if the board is full
    def isBoardFull(self):
        return len(self.moves['x']) + len(self.moves['o']) >= 225
    
    # gets the number of positions left on the board
    def getNumPosLeft(self):
        return 225 - len(self.moves['x']) - len(self.moves['o'])
    
    def isInSquare(self, cell, center = (7,7), radius = 3):
        if((cell[0] > center[0] + radius) or (cell[0] < center[0] - radius)) or ((cell[1] > center[1] + radius) or (cell[1] < center[1] - radius)):
            return False
        return True
    
    def getDirection(self, start, end):
        distance = tuple(map(operator.sub, start, end))
        norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
        direction = [round(distance[0] / norm), round(distance[1] / norm)]
        return direction
    
    def isOutOfRange(self, cell):
        return not(cell[0] >= 0 and cell[0] < 15 and cell[1] >= 0 and cell[1] < 15)
    
    def autoBlock(self, player):
        playerMoves_temp = self.moves[player].copy()
        opponentMoves_temp = self.moves['x' if player == 'o' else 'o'].copy()
        checkedMoves = []

        for move in playerMoves_temp:
            neighbours = self.getNeighbours(move)
            checkedNeighbours = []

            for neighbour in neighbours:
                if neighbour in checkedNeighbours:
                    continue
            
                if neighbour in playerMoves_temp:
                    direction = self.getDirection(move, neighbour)
                    length = 1
                    isHeadBlocked = False
                    isTailBlocked = False
                    isHeadBroken = False
                    isTailBroken = False
                    
                    stop = False

                    head = tuple(map(operator.add, move, direction))

                    if head in checkedMoves:
                        stop = True

                    if self.isOutOfRange(head) or head in opponentMoves_temp:
                        isHeadBlocked = True
                    elif head not in playerMoves_temp and not isHeadBroken:
                        isHeadBroken = True
                        head = tuple(map(operator.add, head, direction))
                        if head in checkedMoves:
                            stop = True
                    
                    while head in playerMoves_temp and not stop:
                        length += 1
                        checkedNeighbours.append(head)
                    
                        head = tuple(map(operator.add, head, direction))
                        if head in checkedMoves:
                            stop = True
                            break
                        if self.isOutOfRange(head) or head in opponentMoves_temp:
                            isHeadBlocked = True
                            break
                        if head not in playerMoves_temp and not isHeadBroken:
                            isHeadBroken = True
                            head = tuple(map(operator.add, head, direction))
                            if head in checkedMoves:
                                stop = True
                                break

                    tail = tuple(map(operator.sub, move, direction))

                    if tail in checkedMoves:
                        stop = True

                    if self.isOutOfRange(tail) or tail in opponentMoves_temp:
                        isTailBlocked = True
                    elif tail not in playerMoves_temp and not isTailBroken:
                        isTailBroken = True
                        tail = tuple(map(operator.sub, tail, direction))
                    if tail in checkedMoves:
                        stop = True
                        break
                    
                    while tail in playerMoves_temp and not stop:
                        length += 1
                        checkedNeighbours.append(tail)
                    
                        tail = tuple(map(operator.sub, tail, direction))
                        if tail in checkedMoves:
                            stop = True
                            break
                        if self.isOutOfRange(tail) or tail in opponentMoves_temp:
                            isTailBlocked = True
                            break
                        if tail not in playerMoves_temp and not isTailBroken:
                            isTailBroken = True
                            tail = tuple(map(operator.sub, tail, direction))
                            if tail in checkedMoves:
                                stop = True
                                break

                    if(stop):
                        continue
                    
                    if length == 4 and (not isTailBlocked and isHeadBlocked) :
                        return tuple(map(operator.add, tail, direction)), direction, 
                    elif length == 4 and (isTailBlocked and not isHeadBlocked):
                        return tuple(map(operator.sub, head, direction)), direction

                    checkedNeighbours.append(neighbour)
                    
            checkedMoves.append(move)
        
        return (-1,-1)
        
    def evaluate(self, player):
        directions = [(-1, -1),(-1, 0), (-1, 1), (0, -1)]
        currentRow = 1   
        state = [[[0] * len(directions) for _ in self.board[0]] for _ in range(2)]
        player_win = False
        opponent_win = False

        for y, row in enumerate(self.board):
            state = state[::-1]

            for x, char in enumerate(row):
                cell = state[currentRow][x]
                for index, (y_diff, x_diff) in enumerate(directions):
                    prev_x = x + x_diff

                    if char == '-':
                        cell[index] = 0
                    elif 0 <= prev_x < len(row) and char == self.board[y + y_diff][prev_x]:
                        cell[index] = state[currentRow + y_diff][prev_x][index] + 1
                    else:
                        cell[index] = 1

                    if cell[index] == 5:
                        if char == player:
                            player_win = True
                        else:
                            opponent_win = True

                        if player_win or opponent_win:
                            return player_win

        return player_win
    
    def getNeighbours(self, cell = None, potentialMoves = False):
        moves = []
        directions = [(1,-1), (-2, 0),(-1, 0), (0, -1), (-1,-1), (2, -2), (0, -2), (-2, -2)]
        
        if(potentialMoves):
            allMoves = self.moves['x'] + self.moves['o']
            for move in allMoves:
                for vector in directions:
                    head = (move[0] + vector[0], move[1] + vector[1])
                    tail = (move[0] - vector[0], move[1] - vector[1])
                    if not self.isOutOfRange(tail) and self.board[tail[0]][tail[1]] == '-':
                        moves.append(tail)
                    if not self.isOutOfRange(head) and self.board[head[0]][head[1]] == '-':
                        moves.append(head)
        else:           
            for vector in directions:
                head = (cell[0] + vector[0], cell[1] + vector[1])
                tail = (cell[0] - vector[0], cell[1] - vector[1])
                if head <= (14,14) and head >= (0,0):
                    moves.append(head)
                if tail <= (14,14) and tail >= (0,0):
                    moves.append(tail)
        return moves
    
    def boardFitness(self, player):
      
        COUNTER = {"counter_2": 0, "open_2": 0, "counter_3": 0, "open_3": 0, "counter_4": 0, "open_4": 0, "win": 0}
        totalScore = 0
        playerMoves_temp = self.moves[player].copy()
        opponentMoves_temp = self.moves['x' if player == 'o' else 'o'].copy()
        checkedMoves = []

        for move in playerMoves_temp:
            neighbours = self.getNeighbours(move)
            checkedNeighbours = []

            for neighbour in neighbours:
                if neighbour in checkedNeighbours:
                    continue
            
                if neighbour in playerMoves_temp:
                    direction = self.getDirection(move, neighbour)
                    length = 1
                    isHeadBlocked = False
                    isTailBlocked = False
                    isHeadBroken = False
                    isTailBroken = False
                    
                    stop = False

                    head = tuple(map(operator.add, move, direction))

                    if head in checkedMoves:
                        stop = True

                    if self.isOutOfRange(head) or head in opponentMoves_temp:
                        isHeadBlocked = True
                    elif head not in playerMoves_temp and not isHeadBroken:
                        isHeadBroken = True
                        head = tuple(map(operator.add, head, direction))
                        if head in checkedMoves:
                            stop = True
                    
                    while head in playerMoves_temp and not stop:
                        length += 1
                        checkedNeighbours.append(head)
                    
                        head = tuple(map(operator.add, head, direction))
                        if head in checkedMoves:
                            stop = True
                            break
                        if self.isOutOfRange(head) or head in opponentMoves_temp:
                            isHeadBlocked = True
                            break
                        if head not in playerMoves_temp and not isHeadBroken:
                            isHeadBroken = True
                            head = tuple(map(operator.add, head, direction))
                            if head in checkedMoves:
                                stop = True
                                break

                    tail = tuple(map(operator.sub, move, direction))

                    if tail in checkedMoves:
                        stop = True

                    if self.isOutOfRange(tail) or tail in opponentMoves_temp:
                        isTailBlocked = True
                    elif tail not in playerMoves_temp and not isTailBroken:
                        isTailBroken = True
                        tail = tuple(map(operator.sub, tail, direction))
                    if tail in checkedMoves:
                        stop = True
                        break
                    
                    while tail in playerMoves_temp and not stop:
                        length += 1
                        checkedNeighbours.append(tail)
                    
                        tail = tuple(map(operator.sub, tail, direction))
                        if tail in checkedMoves:
                            stop = True
                            break
                        if self.isOutOfRange(tail) or tail in opponentMoves_temp:
                            isTailBlocked = True
                            break
                        if tail not in playerMoves_temp and not isTailBroken:
                            isTailBroken = True
                            tail = tuple(map(operator.sub, tail, direction))
                            if tail in checkedMoves:
                                stop = True
                                break

                    if(stop):
                        continue

                    if not isTailBlocked and not isHeadBlocked:
                        moveType = "open_"
                    elif (not isTailBlocked and isHeadBlocked) or (isTailBlocked and not isHeadBlocked):
                        moveType = "counter_"
                    else:
                        moveType = "block"

                    if (length < 5 and length > 1) and moveType != "block":
                        tRank = moveType + str(length)
                        COUNTER[tRank] += 1
                    elif length == 4 and moveType == "block" and (isTailBroken or isHeadBroken):
                        COUNTER["counter_4"] += 1
                    elif length >= 5 and self.evaluate(player):
                         COUNTER["win"] += 1

                    checkedNeighbours.append(neighbour)
                    
            checkedMoves.append(move)
        
        for key in MOVE_VALUES:
            score = MOVE_VALUES[key] * COUNTER[key]
            totalScore = totalScore + score

        return (totalScore, COUNTER)
    


    