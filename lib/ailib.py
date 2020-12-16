from math import inf as infinity
from random import choice
import platform
import time
from os import system


class movePredictor:
    def __init__(self,BOARD):
        self.HUMAN = 0
        self.COMP = 1
        self.board = BOARD

    def wins(self,state,player):
        win_state = [
            [state[0][0], state[0][1], state[0][2]],
            [state[1][0], state[1][1], state[1][2]],
            [state[2][0], state[2][1], state[2][2]],
            [state[0][0], state[1][0], state[2][0]],
            [state[0][1], state[1][1], state[2][1]],
            [state[0][2], state[1][2], state[2][2]],
            [state[0][0], state[1][1], state[2][2]],
            [state[2][0], state[1][1], state[0][2]],
        ]
        if [player, player, player] in win_state:
            return True
        else:
            return False

    def evaluate(self,state):
            if self.wins(state, self.COMP):
                score = +1
            elif self.wins(state, self.HUMAN):
                score = -1
            else:
                score = 0

            return score

    def game_over(self,state):
        return self.wins(state, self.HUMAN) or self.wins(state, self.COMP)

    
    def empty_cells(self,state):
        cells = []
        for x, row in enumerate(state):
            for y, cell in enumerate(row):
                if cell == -1:
                    cells.append([x, y])
        return cells

    def minimax(self,state, depth, player):
        if player == self.COMP:
            best = [-1, -1, -infinity]
        else:
            best = [-1, -1, +infinity]

        if depth == 0 or self.game_over(state):
            score = self.evaluate(state)
            return [-1, -1, score]

        for cell in self.empty_cells(state):
            x, y = cell[0], cell[1]
            state[x][y] = player
            if player==0:
                score = self.minimax(state, depth - 1, 1)
            else:
                score = self.minimax(state, depth - 1, 0)
            state[x][y] = -1
            score[0], score[1] = x, y

            if player == self.COMP:
                if score[2] > best[2]:
                    best = score  # max value
            else:
                if score[2] < best[2]:
                    best = score  # min value
        return best

    def predictMove(self):
        depth = len(self.empty_cells(self.board))
        move = self.minimax(self.board, depth, self.COMP) 
        return move