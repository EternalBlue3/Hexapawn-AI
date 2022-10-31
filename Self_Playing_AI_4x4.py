import pygame, sys
from copy import deepcopy

pygame.init()
red = pygame.Color(255,0,0)
white = pygame.Color(255,255,255)
black = pygame.Color(0,0,0)
pygame.display.set_caption('Hexapawn AI')
width, height = 600,600
game_window = pygame.display.set_mode((width, height))

def opposite(num):
    if num == 0:
        return 3
    if num == 1:
        return 2
    if num == 2:
        return 1
    if num == 3:
        return 0
    
def neg_switch_player(player):
    if player == "RP":
        return "BP"
    else:
        return "RP"

def set_pawns():
    global game_window, bs, board
    for y in range(bs):
        for x in range(bs):
            if board[y][x] == "BP":
                game_window.blit( blue_pawn, ( (width/bs)*x, (height/bs)*opposite(y) ))
            if board[y][x] == "RP":
                game_window.blit( red_pawn, ( (width/bs)*x , (height/bs)*opposite(y) ))

def build_lines():
    global game_window
    for x in range(1,bs):
        pygame.draw.line(game_window, black, (width/bs * x, 0), (width/bs * x, height), 7)
        pygame.draw.line(game_window, black, (0, height/bs * x), (width, height/bs * x), 7)

def get_possible_moves(board,player):
    possible_moves = []
    if player == "BP":
        forward = 1
    if player == "RP":
        forward = -1
    
    for y in range(4):
        for x in range(4):
            if board[y][x] == player:
                if player == "BP":
                    if x-1 != -1 and y+forward != 4:
                        if board[y+forward][x-1] == "RP":
                            possible_moves.append([x,y,x-1,y+forward])
                    if x+1 != 4 and y+forward != 4:
                        if board[y+forward][x+1] == "RP":
                            possible_moves.append([x,y,x+1,y+forward])
                            
                    if y+1 != 4:
                        if board[y+forward][x] == " ":
                            possible_moves.append([x,y,x,y+forward])
                            
                if player == "RP":
                    if x-1 != -1 and y+forward != 4:
                        if board[y+forward][x-1] == "BP":
                            possible_moves.append([x,y,x-1,y+forward])
                    if x+1 != 4 and y+forward != 4:
                        if board[y+forward][x+1] == "BP":
                            possible_moves.append([x,y,x+1,y+forward])
                            
                    if y+1 != -1:
                        if board[y+forward][x] == " ":
                            possible_moves.append([x,y,x,y+forward])
                    
    return possible_moves

def make_move(board,move,player):
    global game_window, width, height
    game_window.fill(white)
    build_lines()
    board[move[1]][move[0]] = " "
    board[move[3]][move[2]] = player
    set_pawns()
    return board

def neg_make_move(new_board,move,player):
    board = deepcopy(new_board)
    board[move[1]][move[0]] = " "
    board[move[3]][move[2]] = player
    return board

def check_for_win(board,player):
    if player == "RP":
        if "RP" in board[0]:
            return True
        if get_possible_moves(board,"BP") == []:
            return True
    if player == "BP":
        if "BP" in board[3]:
            return True
        if get_possible_moves(board,"RP") == []:
            return True
    return False

TRANSPOSITION_TABLE = {}

def store(table, board, alpha, beta, best, depth):
    if best[1] <= alpha:
        flag = 'UPPERCASE'
    elif best[1] >= beta:
        flag = 'LOWERCASE'
    else:
        flag = 'EXACT'

    table[str(board)] = [best, flag, depth]

def negamax(board_, depth, turn, alpha, beta):
    alpha_org = alpha
    if str(board_) in TRANSPOSITION_TABLE:
        tt_entry = TRANSPOSITION_TABLE[str(board_)]
        if tt_entry[2] >= depth:
            if tt_entry[1] == 'EXACT':
                return tt_entry[0]
            elif tt_entry[1] == 'LOWERCASE':
                alpha = max(alpha, tt_entry[0][1])
            elif tt_entry[1] == 'UPPERCASE':
                beta = min(beta, tt_entry[0][1])

            if alpha >= beta:
                return tt_entry[0]
    
    if check_for_win(board_, neg_switch_player(turn)): return None, -(16+depth)
    if depth == 0: return get_possible_moves(board_,turn)[0], (depth)
    
    best_score = -200
    
    for move in get_possible_moves(board_,turn):
        score = -negamax(neg_make_move(board_,move,turn), depth - 1, neg_switch_player(turn), -beta, -alpha)[1]
        alpha = max(alpha,score)
        if score > best_score:
            best_score, best_move = score, move
        if alpha >= beta:
            break
            
    store(TRANSPOSITION_TABLE, board_, alpha_org, beta, [best_move,best_score], depth)
            
    return best_move, best_score

# Build board
bs = 4 # bs = Board Size
board = [["BP" for x in range(bs)]]
for x in range(bs-2):
    board.append([" " for x in range(bs)])
board.append(["RP" for x in range(bs)])

fps_controller = pygame.time.Clock()

game_window.fill(white)

# Draw game board lines
build_lines()

# Load sprites with correct sizes
tile_size = (width/bs,height/bs)
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
    
    move = negamax(board,20,"BP",-10000,10000)[0]
    board = make_move(board,move,"BP")
    pygame.display.update()
    
    if check_for_win(board,"BP"):
        print("Blue Wins!")
        pygame.quit()
        sys.exit()
    
    fps_controller.tick(1)
    
    move = negamax(board,20,"RP",-10000,10000)[0]
    board = make_move(board,move,"RP")
    pygame.display.update()
    
    if check_for_win(board,"RP"):
        print("Red Wins!")
        pygame.quit()
        sys.exit()
    
    pygame.display.update()
    fps_controller.tick(1)
