from piece import *
import pygame

# verifica ganhador
def find_winner(board):
    kings = []
    for i in range(8):
        for j in range(8):
            if isinstance(board[i][j], Rei):
                kings.append(board[i][j])
    
    if len(kings) == 2:
        return False
    else:
        pygame.quit()        
        return "porra, pika! as {kings[0].team} venceram !"
        