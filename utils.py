def verify_diagonal(x, y):
    directions = [[-1,-1],[1, -1], [1, 1], [-1, 1]]
    pos_coords = []
    x_ini, y_ini = x, y        
    
    for direction in directions:
        x, y = x_ini, y_ini
    
        while True:
            i = direction[0] + x
            j = direction[1] + y        
    
            if i in (8, -1) or j in (8, -1):
                break
    
            pos_coords.append([i,j])
            x, y = i, j
    
    return pos_coords

def verify_diagonal_till_piece(x, y, coords_with_pieces):
    directions = [[-1,-1],[1, -1], [1, 1], [-1, 1]]
    pos_coords = []
    x_ini, y_ini = x, y        
    
    for direction in directions:
        x, y = x_ini, y_ini
    
        while True:
            i = direction[0] + x
            j = direction[1] + y        
    
            if i in (8, -1) or j in (8, -1):
                break
            
            pos_coords.append([i,j])
            
            if [i,j] in coords_with_pieces:
                break
            
            x, y = i, j
    
    return pos_coords


def verify_cross(x, y):
    directions = [[-1, 0], [0, -1], [1, 0], [0, 1]]
    pos_coords = []
    x_ini, y_ini = x, y
    
    for direction in directions:
        x, y = x_ini, y_ini
    
        while True:
            i = direction[0] + x
            j = direction[1] + y
    
            if i in (8, -1) or j in (8, -1):
                break
    
            pos_coords.append([i,j])
            x, y = i, j
    
    return pos_coords

def verify_cross_till_piece(x, y, coords_with_pieces):
    directions = [[-1, 0], [0, -1], [1, 0], [0, 1]]
    pos_coords = []
    x_ini, y_ini = x, y
    
    for direction in directions:
        x, y = x_ini, y_ini
        
        while True:
            i = direction[0] + x
            j = direction[1] + y
            
            if i in (8, -1) or j in (8, -1):
                break
            
            pos_coords.append([i,j])
            x, y = i, j

            if [i,j] in coords_with_pieces:
                break

    return pos_coords

def verify_Peao(pos_coords, coords_with_pieces):
    moves = []

    print(pos_coords)
    print(coords_with_pieces)
    
    
    if len(pos_coords)==3:
        # dois pra frente se for o peão estiver na sua primeira linha 
        if pos_coords[0][1] == 5:
            moves.append([ pos_coords[2][0], pos_coords[2][1] - 1 ])
        elif pos_coords[0][1] == 2:
            moves.append( [pos_coords[2][0], pos_coords[2][1] + 1])

        for x in range(2):
            if pos_coords[x] in coords_with_pieces:
                moves.append(pos_coords[x])
        
        if pos_coords[2] in coords_with_pieces:
            return moves
        
        moves.append(pos_coords[2])    
        
        return moves
    else:
        if pos_coords[0][1] == 5:
            moves.append([ pos_coords[1][0], pos_coords[1][1] - 1 ])
        elif pos_coords[0][1] == 2:
            moves.append( [pos_coords[1][0], pos_coords[1][1] + 1])

        if pos_coords[0] in coords_with_pieces:
            moves.append(pos_coords[0])
        
        if pos_coords[1] in coords_with_pieces:
            return moves
        
        moves.append(pos_coords[1])
        return moves

def change_Peao(board):
    for i in range(8):
        if isinstance(board[0][i], Peao):
            return (0, i)
        if isinstance(board[7][i], Peao):
            return (7, i)
         




def filter_coords(pos_coords):
    n_pos_coords = []
    
    for coords in pos_coords:
        
        if coords[0] > 7 or coords[0] < 0 or coords[1] > 7 or coords[1] < 0:
            n_pos_coords.append(coords)
    
    return [x for x in pos_coords if not (x in n_pos_coords)]

def change_team(team):
    if team == "brancas":
        return "pretas"
    else:
        return "brancas"


import pygame

def change_screen(x_mouse, y_mouse, screen, tamanho, atual):
    if(x_mouse > 150 and x_mouse < 450):
        if y_mouse > 150 and y_mouse < 230:
            atual = "board"

    if("home" == atual):
        pygame.draw.rect(screen, (255,255,255), pygame.Rect((150,150), (200,80)) )

    if("board" == atual):
        print_board(screen, tamanho)

def get_evento():
    x_mouse = None 
    y_mouse = None
    run = True 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x_mouse, y_mouse = pygame.mouse.get_pos()
    
    return x_mouse, y_mouse, run