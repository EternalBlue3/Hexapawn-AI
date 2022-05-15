import pygame, sys
from copy import deepcopy

pygame.init()
red = pygame.Color(255,0,0)
white = pygame.Color(255,255,255)
black = pygame.Color(0,0,0)
pygame.display.set_caption('Hexapawn AI')
width, height = 600,600
game_window = pygame.display.set_mode((width, height))

def opposite(num,middle):
    if num == middle:
        return middle
    if num > middle:
        return middle - 0.5*num
    if num < middle:
        return num + 2*middle
    
def neg_switch_player(player):
    if player == "red":
        return "blue"
    else:
        return "red"

def set_pawns():
    global game_window, bs, board
    for y in range(bs):
        for x in range(bs):
            if board[y][x] == "BP":
                game_window.blit( blue_pawn, ( (width/bs)*x, (height/bs)*opposite(y,1) ))
            if board[y][x] == "RP":
                game_window.blit( red_pawn, ( (width/bs)*x , (height/bs)*opposite(y,1) ))

def build_lines():
    global game_window
    for x in range(1,bs):
        pygame.draw.line(game_window, black, (width/bs * x, 0), (width/bs * x, height), 7)
        pygame.draw.line(game_window, black, (0, height/bs * x), (width, height/bs * x), 7)

def get_possible_moves(board,player):
    global bs
    possible_moves = []
    if player == "blue":
        player = "BP"
        forward = 1
    if player == "red":
        player = "RP"
        forward = -1
    
    for y in range(bs):
        for x in range(bs):
            if board[y][x] == player:
                if player == "BP":
                    if x-1 != -1 and y+forward != 3:
                        if board[y+forward][x-1] == "RP":
                            possible_moves.append([x,y,x-1,y+forward])
                    if x+1 != 3 and y+forward != 3:
                        if board[y+forward][x+1] == "RP":
                            possible_moves.append([x,y,x+1,y+forward])
                            
                    if y+1 != 3:
                        if board[y+forward][x] == " ":
                            possible_moves.append([x,y,x,y+forward])
                            
                if player == "RP":
                    if x-1 != -1 and y+forward != 3:
                        if board[y+forward][x-1] == "BP":
                            possible_moves.append([x,y,x-1,y+forward])
                    if x+1 != 3 and y+forward != 3:
                        if board[y+forward][x+1] == "BP":
                            possible_moves.append([x,y,x+1,y+forward])
                            
                    if y+1 != -1:
                        if board[y+forward][x] == " ":
                            possible_moves.append([x,y,x,y+forward])
                    
    return possible_moves

def make_move(board,move,player):
    global game_window, bs, width, height
    if player == "blue":
        player = "BP"
    if player == "red":
        player = "RP"
    game_window.fill(white)
    build_lines()
    board[move[1]][move[0]] = " "
    board[move[3]][move[2]] = player
    set_pawns()
    return board

def neg_make_move(board,move,player):
    if player == "blue":
        player = "BP"
    if player == "red":
        player = "RP"
    board[move[1]][move[0]] = " "
    board[move[3]][move[2]] = player
    return board

def check_for_win(board,player):
    if player == "blue":
        player = "BP"
    if player == "red":
        player = "RP"
    
    if player == "RP":
        if "RP" in board[0]:
            return True
        if get_possible_moves(board,"blue") == []:
            return True
    if player == "BP":
        if "BP" in board[2]:
            return True
        if get_possible_moves(board,"red") == []:
            return True
    return False

def negamax(board_, depth, turn):
    
    if check_for_win(board_, turn): return None, (9+depth)  # Return positive score if maximizing player
    
    if check_for_win(board_, neg_switch_player(turn)): return None, -(9 + depth)  # Return negative score if minimizing player wins
    
    if depth == 0: return get_possible_moves(board_,turn)[0], (4+depth)
    
    best_score = -20  # Initiate with less than smallest possible score
    
    for move in get_possible_moves(board_,turn):  # Go through all empty squares on board
        
        board_ = deepcopy(board_)
        board_ = neg_make_move(board_,move,turn)
        
        score = -negamax(board_, depth - 1, neg_switch_player(turn))[1]  # Recursive call to go through all child nodes
        
        if score > best_score: 
            best_score, best_move = score, move  # If score is larger than previous best, update score
            
    return best_move, best_score  # Return the best move and its corresponding score

# Build board
bs = 3 # bs = Board Size
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
    
    move = negamax(board,10,"blue")[0]
    board = make_move(board,move,"blue")
    pygame.display.update()
    
    if check_for_win(board,"blue"):
        print("Blue Wins!")
        pygame.quit()
        sys.exit()
    
    fps_controller.tick(1)
    
    move = negamax(board,10,"red")[0]
    board = make_move(board,move,"red")
    pygame.display.update()
    
    if check_for_win(board,"red"):
        print("Red Wins!")
        pygame.quit()
        sys.exit()
    
    pygame.display.update()
    fps_controller.tick(1)
