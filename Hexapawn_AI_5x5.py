# Blue Pawn = 1
# Red Pawn = -1

import pygame, sys, time, math
from copy import deepcopy
from collections import OrderedDict

pygame.init()
white = pygame.Color(255,255,255)

pygame.display.set_caption('Hexapawn AI')
width, height = 605,605
game_window = pygame.display.set_mode((width, height))

def set_pawns(board):
    global game_window
    for y, row in enumerate(board):
        for x, pawn in enumerate(row):
            if pawn == 1:
                game_window.blit(blue_pawn,((width/5)*x,(height/5)*(4-y)))
            if pawn == -1:
                game_window.blit(red_pawn,((width/5)*x,(height/5)*(4-y)))
    pygame.display.update()

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
                            
                elif player == -1:
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
    global BG_Image
    game_window.blit(BG_Image,(0,0))
    board[move[1]][move[0]] = 0
    board[move[3]][move[2]] = player
    set_pawns(board)
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

def get_player_move(mouse_x, mouse_y):
    column = 4 - mouse_y // 121
    row = mouse_x // 121
    return row, column

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
    TT = LRUCache(16777216)
    best_score = -math.inf
    
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
    
    best_score = -math.inf
    
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

# Define board, fps_controller, background, and pawns
board = [[1,1,1,1,1],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[-1,-1,-1,-1,-1]]
fps_controller = pygame.time.Clock()

# Set Background Image
BG_Image = pygame.image.load('Hexapawn_Background.png')
game_window.blit(BG_Image,(0,0))

# Load sprites with correct sizes
tile_size = (width/5,height/5)
blue_pawn = pygame.transform.scale(pygame.image.load("blue_pawn_2.png"), tile_size)
red_pawn = pygame.transform.scale(pygame.image.load("red_pawn_2.png"), tile_size)

# Draw the pawns to the board
set_pawns(board)
pygame.display.flip()

def main():
    global board
    move_dictionary = [(0,0), (1,0), (2,0), (3,0), (4,0), (0,1), (1,1), (2,1), (3,1), (4,1), (0,2), (1,2), (2,2), (3,2), (4,2), (0,3), (1,3), (2,3), (3,3), (4,3), (0,4), (1,4), (2,4), (3,4), (4,4)]
    current_player = 1
    player_move = []
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

            if event.type == pygame.MOUSEBUTTONDOWN and current_player == -1:
                mouseX, mouseY = pygame.mouse.get_pos()
                moves = get_possible_moves(board,-1)
                playerX,playerY = get_player_move(mouseX,mouseY)

                if len(player_move) == 2:
                    if any(player_move[0] == x[0] and player_move[1] == x[1] and playerX == x[2] and playerY == x[3] for x in moves):
                        player_move.append(playerX)
                        player_move.append(playerY)
                    else:
                        player_move = [] # Redefine player move
                        game_window.blit(BG_Image,(0,0)) # Remove transparent circles
                        set_pawns(board) # Remove transparent circles

                if len(player_move) == 0:
                    if any(playerX == x[0] and playerY == x[1] for x in moves):
                        player_move.append(playerX)
                        player_move.append(playerY)

                    for x in moves:
                        if playerX == x[0] and playerY == x[1]:
                            transparency_surface = pygame.Surface((width,height), pygame.SRCALPHA)
                            pygame.draw.circle(transparency_surface,(220,220,220,200),(x[2]*121+61,(4-x[3])*121+61),19,width=0)
                            game_window.blit(transparency_surface, (0,0))
                    pygame.display.update()

                if len(player_move) == 4:
                    if player_move in get_possible_moves(board,-1):
                        board = make_move(board,player_move,-1)
                        player_move, current_player = [], 1
                        pygame.display.update()

                if check_for_win(board,-1):
                    print("Red Wins!")
                    time.sleep(5)
                    pygame.quit()
                    sys.exit()

        if current_player == 1:
            start = time.time()
            move = solve(board,80,1,-10000,10000)
            print("Move: ",move[0],"    Score: ",move[1])
            print("Time to generate move:",time.time()-start,"\n")
            board = make_move(board,move[0],1)

            if check_for_win(board,1):
                print("Blue Wins!")
                time.sleep(5)
                pygame.quit()
                sys.exit()

            current_player = -1

        pygame.display.update()
        fps_controller.tick(18)
        
if __name__ == '__main__':
    main()
