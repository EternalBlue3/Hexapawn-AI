import pygame, sys

# Set Background Image
BG_Image = pygame.image.load('./assets/Hexapawn_Background.png')
blue_pawn = pygame.transform.scale(pygame.image.load("./assets/blue_pawn.png"), (121,121))
red_pawn = pygame.transform.scale(pygame.image.load("./assets/red_pawn.png"), (121,121))

def set_pawns(game_window,board,width,height):
    for y, row in enumerate(board):
        for x, pawn in enumerate(row):
            if pawn == 1:
                game_window.blit(blue_pawn,((width/5)*x,(height/5)*(4-y)))
            if pawn == -1:
                game_window.blit(red_pawn,((width/5)*x,(height/5)*(4-y)))
    pygame.display.update()
    
# Show users possible moves with transparent circle
def show_player_moves(game_window, width, height, x, y):
    transparency_surface = pygame.Surface((width,height), pygame.SRCALPHA)
    pygame.draw.circle(transparency_surface,(220,220,220,200),(x*121+61,(4-y)*121+61),19,width=0)
    game_window.blit(transparency_surface, (0,0))
    
def make_move(game_window,board,move,player,bgimage,width,height):
    game_window.blit(bgimage,(0,0))
    board[move[1]][move[0]] = 0
    board[move[3]][move[2]] = player
    set_pawns(game_window,board,width,height)
    return board
    
def start_menu(game_window,width,height):
    fps = pygame.time.Clock()
    white = pygame.Color(255,255,255)
    black = pygame.Color(0,0,0)
    
    # Small versions of the pawn images
    blue_pawn = pygame.transform.scale(pygame.image.load("./assets/blue_pawn.png"), (45,45))
    red_pawn = pygame.transform.scale(pygame.image.load("./assets/red_pawn.png"), (45,45))
    
    # Draw the menu options
    game_window.fill(white)
    
    title_font = pygame.font.SysFont("Arial", 72)
    title_text = title_font.render("Hexapawn AI", True, black)

    player_font = pygame.font.SysFont("Arial", 44)
    player1_text = player_font.render("Blue", True, black)
    player2_text = player_font.render("Red ", True, black)

    quit_font = pygame.font.SysFont("Arial", 32)
    quit_text = quit_font.render("Quit", True, black)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                if 220 <= mouseX <= 381 and 222 <= mouseY <= 273:
                    return 1
                elif 220 <= mouseX <= 381 and 322 <= mouseY <= 373:
                    return -1
                elif 274 <= mouseX <= 332 and 424 <= mouseY <= 456:
                    pygame.quit()
                    sys.exit()

        # Display visuals and update the screen
        game_window.fill(white)
        game_window.blit(title_text, (width/2 - title_text.get_width()/2, 50))
        
        player1_rect = player1_text.get_rect(center=(width/2, 250))
        pygame.draw.rect(game_window, (173,216,230), pygame.Rect(220, 222, 161, 51),  0,  5)
        game_window.blit(player1_text, player1_rect)
        
        player2_rect = player2_text.get_rect(center=(width/2, 350))
        pygame.draw.rect(game_window, (255,0,0), pygame.Rect(220, 322, 161, 51), 0, 5)
        game_window.blit(player2_text, player2_rect)
        
        game_window.blit(quit_text, (width/2 - quit_text.get_width()/2, 440))
        
        pygame.display.update()
        fps.tick(24)