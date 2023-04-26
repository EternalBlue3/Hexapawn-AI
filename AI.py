import math, json
from copy import deepcopy
from collections import OrderedDict
from ast import literal_eval
from Game import get_possible_moves, check_for_win

dictionary = json.loads(''.join(open("Dictionary.txt","r").readlines()))

def negamax_make_move(new_board,move,player):
    board = deepcopy(new_board)
    board[move[1]][move[0]] = 0
    board[move[3]][move[2]] = player
    return board

class LRUCache(OrderedDict):

    def __init__(self, maxsize=256, *args, **kwds):
        self.maxsize = maxsize
        super().__init__(*args, **kwds)

    def __getitem__(self, key):
        value = super().__getitem__(key)
        self.move_to_end(key)
        return value

    def __setitem__(self, key, value):
        if key in self:
            self.move_to_end(key)
        super().__setitem__(key, value)
        if len(self) > self.maxsize:
            oldest = next(iter(self))
            del self[oldest]
            
def get_tt_entry(value, UB=False, LB=False):
    return {'value': value, 'UB': UB, 'LB': LB}

def solve(board, depth, turn, alpha, beta, turns_taken, dictionary):
    if turns_taken <= 2:
        return literal_eval(dictionary[str(board)])
    
    TT = LRUCache(16777216)
    best_score = -math.inf
    
    for move in get_possible_moves(board,turn):
        score = -negamax(negamax_make_move(board,move,turn), depth - 1, -turn, -beta, -alpha, TT)
        alpha = max(alpha,score)
        if score > best_score:
            best_score, best_move = score, move
        if alpha >= beta:
            break
                
    return best_move, best_score

def negamax(board, depth, turn, alpha, beta, TT):
    alpha_original = alpha
    board_string = str(board)
    
    if board_string in TT:
        entry = TT[board_string]
        if entry['LB']:
            alpha = max(alpha, entry['value'])  # lower bound stored in TT
        elif entry['UB']:
            beta = min(beta, entry['value'])    # upper bound stored in TT
        else:
            return entry['value']               # exact value stored in TT
        if alpha >= beta:
            return entry['value']               # cut-off (from TT)
    
    if check_for_win(board, -turn): return -(16+depth)
    if depth == 0: return depth
    
    best_score = -math.inf
    
    for move in get_possible_moves(board,turn):
        score = -negamax(negamax_make_move(board,move,turn), depth - 1, -turn, -beta, -alpha, TT)
        alpha = max(alpha,score)
        if score > best_score:
            best_score = score
        if alpha >= beta:
            break
                
    if best_score <= alpha_original:
        TT[board_string] = get_tt_entry(best_score, UB=True)
    elif best_score >= beta:
        TT[board_string] = get_tt_entry(best_score, LB=True)
    else:
        TT[board_string] = get_tt_entry(best_score)       # store exact in TT
    
    return best_score