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

def translate_player_move(mouse_x, mouse_y):
    column = 4 - mouse_y // 121
    row = mouse_x // 121
    return row, column