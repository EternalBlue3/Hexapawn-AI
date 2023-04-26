import pygame, sys, time
from Game import get_possible_moves, check_for_win, translate_player_move
from AI import solve, dictionary
from GUI import set_pawns, show_player_moves, blue_pawn, red_pawn, BG_Image, start_menu, make_move

pygame.init()
white = pygame.Color(255,255,255)
pygame.display.set_caption('Hexapawn AI')
width, height = 605,605
game_window = pygame.display.set_mode((width, height))

# Define board, fps_controller, background, and pawns
fps_controller = pygame.time.Clock()

def main():
    global board
    
    current_player = 1
    player_move = []
    turns_taken = 0
    
    player_option = start_menu(game_window,width,height)
    opponent = -player_option
    board = [[1,1,1,1,1],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[-1,-1,-1,-1,-1]]
            
    # Set Background Image and draw pawns
    game_window.blit(BG_Image,(0,0))
    set_pawns(game_window,board,width,height)

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

            if event.type == pygame.MOUSEBUTTONDOWN and current_player == player_option:
                mouseX, mouseY = pygame.mouse.get_pos()
                moves = get_possible_moves(board,player_option)
                playerX,playerY = translate_player_move(mouseX,mouseY) # Translate from X,Y to board position

                # Check where to draw possible moves, and make sure the player can't make an illegal move
                # Also make sure only the correct possible moves are shown for the player
                if len(player_move) == 2:
                    if any(player_move[0] == x[0] and player_move[1] == x[1] and playerX == x[2] and playerY == x[3] for x in moves):
                        player_move.append(playerX)
                        player_move.append(playerY)
                    else:
                        player_move = [] # Redefine player move
                        game_window.blit(BG_Image,(0,0)) # Remove transparent circles
                        set_pawns(game_window,board,width,height) # Remove transparent circles

                if len(player_move) == 0:
                    if any(playerX == x[0] and playerY == x[1] for x in moves):
                        player_move.append(playerX)
                        player_move.append(playerY)

                    for x in moves:
                        if playerX == x[0] and playerY == x[1]:
                            show_player_moves(game_window,width,height,x[2],x[3])

                if len(player_move) == 4:
                    if player_move in get_possible_moves(board,player_option):
                        board = make_move(game_window,board,player_move,player_option,BG_Image,width,height) # Pass game window, current board, player's move, player, background image, width and height of window
                        player_move = []
                        current_player = -current_player
                        turns_taken += 1

                if check_for_win(board,player_option):
                    print("You Win!")
                    time.sleep(5)
                    pygame.quit()
                    sys.exit()

                pygame.display.update()

        if current_player == opponent:
            start = time.time()
            move = solve(board,80,opponent,-10000,10000,turns_taken,dictionary)
            print("Move: ",move[0],"    Score: ",move[1])
            print("Time to generate move:",time.time()-start,"\n")
            board = make_move(game_window,board,move[0],opponent,BG_Image,width,height)

            if check_for_win(board,opponent):
                print("Opponent Wins!")
                time.sleep(5)
                pygame.quit()
                sys.exit()

            current_player = -current_player
            turns_taken += 1
            
        pygame.display.update()
        fps_controller.tick(24)
        
if __name__ == '__main__':
    main()