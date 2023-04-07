import pygame, sys
from copy import deepcopy
from collections import OrderedDict

# Blue Pawn = 1
# Red Pawn = -1

pygame.init()
red = pygame.Color(255,0,0)
white = pygame.Color(255,255,255)
black = pygame.Color(0,0,0)
pygame.display.set_caption('Hexapawn AI')
width, height = 600,600
game_window = pygame.display.set_mode((width, height))

def set_pawns():
    global game_window, board
    for y in range(5):
        for x in range(5):
            if board[y][x] == 1:
                game_window.blit(blue_pawn,((width/5)*x,(height/5)*(4-y)))
            if board[y][x] == -1:
                game_window.blit(red_pawn,((width/5)*x,(height/5)*(4-y)))

def build_lines():
    global game_window
    for x in range(1,5):
        pygame.draw.line(game_window, black,(width/5 * x, 0),(width/5 * x, height),7)
        pygame.draw.line(game_window, black,(0, height/5 * x),(width, height/5 * x),7)

def get_possible_moves(board,player):
    possible_moves = []
    forward = player
    
    for y in range(5):
        for x in range(5):
            if board[y][x] == player:
                if player == 1:
                    if x-1 != -1 and y+forward != 5:
                        if board[y+forward][x-1] == -1:
                            possible_moves.append([x,y,x-1,y+forward])
                    if x+1 != 5 and y+forward != 5:
                        if board[y+forward][x+1] == -1:
                            possible_moves.append([x,y,x+1,y+forward])
                            
                    if y+1 != 5:
                        if board[y+forward][x] == 0:
                            possible_moves.append([x,y,x,y+forward])
                            
                if player == -1:
                    if x-1 != -1 and y+forward != 5:
                        if board[y+forward][x-1] == 1:
                            possible_moves.append([x,y,x-1,y+forward])
                    if x+1 != 5 and y+forward != 5:
                        if board[y+forward][x+1] == 1:
                            possible_moves.append([x,y,x+1,y+forward])
                            
                    if y+1 != -1:
                        if board[y+forward][x] == 0:
                            possible_moves.append([x,y,x,y+forward])
                    
    return possible_moves

def make_move(board,move,player):
    global game_window, width, height
    game_window.fill(white)
    build_lines()
    board[move[1]][move[0]] = 0
    board[move[3]][move[2]] = player
    set_pawns()
    return board

def neg_make_move(new_board,move,player):
    board = deepcopy(new_board)
    board[move[1]][move[0]] = 0
    board[move[3]][move[2]] = player
    return board

def check_for_win(board,player):
    if player == -1:
        if -1 in board[0]:
            return True
        if get_possible_moves(board,1) == []:
            return True
    if player == 1:
        if 1 in board[4]:
            return True
        if get_possible_moves(board,-1) == []:
            return True
    return False

########## AI ##########
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

def solve(board, depth, turn, alpha, beta):
    TT = LRUCache(4194304)
    best_score = -200
    
    for move in get_possible_moves(board,turn):
        score = -negamax(neg_make_move(board,move,turn), depth - 1, -turn, -beta, -alpha, TT)
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
    
    best_score = -200
    
    for move in get_possible_moves(board,turn):
        score = -negamax(neg_make_move(board,move,turn), depth - 1, -turn, -beta, -alpha, TT)
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

# Build board
board = [[1 for x in range(5)]]
for x in range(3):
    board.append([0 for x in range(5)])
board.append([-1 for x in range(5)])

fps_controller = pygame.time.Clock()
game_window.fill(white)

# Draw game board lines
build_lines()

# Load sprites with correct sizes
tile_size = (width/5,height/5)
blue_pawn = pygame.transform.scale(pygame.image.load("blue_pawn.png"), tile_size)
red_pawn = pygame.transform.scale(pygame.image.load("red_pawn.png"), tile_size)

# Draw the pawns to the board
set_pawns()

pygame.display.update()
fps_controller.tick(1)

while True:
    for event in pygame.event.get():

      # if user clicks the X or they type esc then the screen will close
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
    
    move = solve(board,220,1,-10000,10000)[0] # Depth is large enough that the program searches through the entire game. Modify the depth to increase or decrease strength.
    board = make_move(board,move,1)
    pygame.display.update()
    
    if check_for_win(board,1):
        print("Blue Wins!")
        pygame.quit()
        sys.exit()
    
    fps_controller.tick(1)
    
    move = solve(board,220,-1,-10000,10000)[0]
    board = make_move(board,move,-1)
    pygame.display.update()
    
    if check_for_win(board,-1):
        print("Red Wins!")
        pygame.quit()
        sys.exit()
    
    pygame.display.update()
    fps_controller.tick(1)
