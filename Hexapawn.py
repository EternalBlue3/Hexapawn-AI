# Blue Pawn = 1
# Red Pawn = -1

import pygame, sys, time
from Game import get_possible_moves, check_for_win
from AI import solve

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

def make_move(board,move,player):
    global BG_Image
    game_window.blit(BG_Image,(0,0))
    board[move[1]][move[0]] = 0
    board[move[3]][move[2]] = player
    set_pawns(board)
    return board

def get_player_move(mouse_x, mouse_y):
    column = 4 - mouse_y // 121
    row = mouse_x // 121
    return row, column

# Define board, fps_controller, background, and pawns
board = [[1,1,1,1,1],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[-1,-1,-1,-1,-1]]
fps_controller = pygame.time.Clock()

# Set Background Image
BG_Image = pygame.image.load('./assets/Hexapawn_Background.png')
game_window.blit(BG_Image,(0,0))

# Load sprites with correct sizes
tile_size = (width/5,height/5)
blue_pawn = pygame.transform.scale(pygame.image.load("./assets/blue_pawn.png"), tile_size)
red_pawn = pygame.transform.scale(pygame.image.load("./assets/red_pawn.png"), tile_size)

# Draw the pawns to the board
set_pawns(board)
pygame.display.flip()

def main():
    global board
    
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