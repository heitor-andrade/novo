from abc import abstractmethod
from utils import *
import pygame
import os
# classes das pecas
class Pecas:
    def __init__(self,team, img):
        # team = brancas | pretas
        self.team = team
        self.img = pygame.image.load(os.path.join('imgs', str(img) +'.png'))
        self.img = pygame.transform.scale(self.img, (56,56))

    @abstractmethod 
    def show_move(self):
        pass


class Peao(Pecas):
    def show_move(self, x, y):
        if self.team == "brancas":
            return filter_coords([[x+1, y-1], [x-1, y-1], [x, y-1]])
        else:
            return filter_coords([[x+1, y+1], [x-1, y+1], [x, y+1]])


class Cavalo(Pecas):
    def show_move(self, x, y):
        directions = [-1, 1]
        pos_coords = []

        for direction in directions:
            i = x + 2*direction
            j1, j2 = y + 1, y - 1
            pos_coords.append([i, j1])
            pos_coords.append([i, j2])

        for direction in directions:
            j = y + 2*direction
            i1, i2 = x + 1, x - 1
            pos_coords.append([i1, j])
            pos_coords.append([i2, j])

        return filter_coords(pos_coords)

    # vai numa direção
    # soma um e tira um na outra

class Bispo(Pecas):
    def show_move(self, x, y):
        return verify_diagonal(x, y)        

class Torre(Pecas):
    def show_move(self, x, y):
        return verify_cross(x, y)

class Rainha(Pecas):
    def show_move(self, x, y):
        return verify_cross(x, y) + verify_diagonal(x, y)

class Rei(Pecas):
    def show_move(self, x, y):
        directions = [[-1,-1],[1, -1], [1, 1], [-1, 1], [-1, 0], [0, -1], [1, 0], [0, 1]]
        for index, direction in enumerate(directions):
            directions[index][0] = direction[0] + x
            directions[index][1] = direction[1] + y
        return filter_coords(directions)
