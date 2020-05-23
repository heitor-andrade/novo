import pygame
from board import Board
from client import Client
from utils import get_evento
import pickle

pygame.init()

board = Board((600,600))
board.print_board()
board.print_pieces()

run = True

client = Client()
pygame.display.update()

CLIENT = int(client.receive())

recebendo = False

while run:
    x_mouse2 = None
    x_mouse1, y_mouse1, run = get_evento()

    if not CLIENT: 
        x_mouse1, y_mouse1, x_mouse2, y_mouse2 = client.receive()
        print('recebi: ', x_mouse1, y_mouse1, x_mouse2, y_mouse2)    
        recebendo = True

    if board.get_first_click(x_mouse1, y_mouse1):

        waitMove = True
        while waitMove:

                if x_mouse2:
                    board.get_second_click(x_mouse2, y_mouse2)
                    waitMove = False
                    
                    if CLIENT and not recebendo:
                        client.send([x_mouse1, y_mouse1, x_mouse2, y_mouse2])
                        print('mandei: ', x_mouse1, y_mouse1, x_mouse2, y_mouse2 )
                        CLIENT = not CLIENT

                    if recebendo:
                        recebendo = False
                        CLIENT = not CLIENT

                x_mouse2, y_mouse2, run = get_evento()

                pygame.display.update()


    pygame.display.update()
    pygame.time.delay(100)

pygame.quit()