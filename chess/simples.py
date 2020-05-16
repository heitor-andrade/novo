import pygame
from piece import Peao
from events import get_evento
from board import Board

pygame.init()
peao = Peao("brancas", "peaob")

board = Board((600,600))
board.print_board()

coord = (4,6)

run = True
while run:
    x_mouse = None
    y_mouse = None

    board.print_piece(peao, coord)

    x_mouse, y_mouse, run = get_evento(x_mouse, y_mouse, run)

    # se clicar em qualquer lugar
    if x_mouse:
        coord = board.get_coord(x_mouse, y_mouse)
        coords, team = peao.show_move(coord)

        waitMove = True
        while waitMove:
            board.print_move(coords, team)
            x_mouse_inicial = x_mouse
            x_mouse, y_mouse, run = get_evento(x_mouse, y_mouse, run)
            new_coord = board.get_coord(x_mouse, y_mouse)
            
            if new_coord in coords:   # se clicar num dos movimentos possíveis
                peao.move(new_coord)
                board.erase_move(coords, coord)
                waitMove = False
                coord = new_coord
            elif x_mouse_inicial != x_mouse: # se clicar em qualquer outro lugar
                waitMove = False
            
            pygame.display.update()


    pygame.display.update()
    pygame.time.delay(100)

pygame.quit()