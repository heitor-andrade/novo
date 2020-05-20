import pygame
from piece import *
from utils import *
from rules import *

class Board:
    
    def __init__(self, tamanho, atual = "home"):
        self.tamanho = tamanho
        self.lado  = int(tamanho[0]/8)
        self.atual = atual
        self.team = "brancas"
        self.rockb = [1,1]
        self.rockp = [1,1]
        self.rockDone = False
        self.rockGoing = False
        self.board = self.make_board()
        self.screen = pygame.display.set_mode(tamanho)
        pygame.display.set_caption("Chess")
        self.load_pieces()
        self.pieces_on_matrix()

    def make_board(self):
        board = []
        for coluna in range (8):
            lista = []
            for linha in range(8):
                valor = (linha, coluna)
                lista.append(None)
            board.append(lista)
        return board

    def print_board(self):   
        for linha in range(8):
            for coluna in range(8):
                rect = pygame.Rect(linha*self.lado, coluna*self.lado, self.lado, self.lado)
                
                if (coluna + linha) % 2:
                    cor = (0,0,0)
                else:
                    cor = (255,255,255)
                
                pygame.draw.rect(self.screen,cor, rect)

    def print_one_piece(self, piece, coord):
        x = coord[0]*self.tamanho[0]/8 + 10
        y = coord[1]*self.tamanho[1]/8 + 10
        self.screen.blit(piece.img, (int(x), int(y)))

    # star-first click
    def get_first_click(self, x_mouse, y_mouse):
        if x_mouse:
            i, j = self.get_coord(x_mouse, y_mouse)
            piece = self.get_piece(i, j)

            if piece and piece.team == self.team:
                self.piece = piece

                if piece:
                    self.i = i
                    self.j = j 
                    x = self.filter_by_pieces(i, j, piece.show_move(i, j))
                    self.pos_coords = list(self.filter_by_team(x))
                    if isinstance(self.piece, Rei):
                        self.verify_rock()
                    self.print_move(self.pos_coords)
                    self.reprint_pieces(x)
                    return True
        
        return False 

    def get_coord(self, x_mouse, y_mouse): # pega coordenada
        x = x_mouse//(self.tamanho[0]/8)
        y = y_mouse//(self.tamanho[1]/8)
        return (int(x),int(y))

    def get_piece(self, i, j): # pega a peça
        piece = self.board[i][j]
        return piece


    def print_move(self, pos_coords): # printa o movimento
        for coord in pos_coords:
            rect = pygame.Rect(coord[0]*self.lado, coord[1]*self.lado,self.lado, self.lado)
            pygame.draw.rect(self.screen, (0,130,0), rect)


    def filter_by_pieces(self, x, y, pos_coords):
        coords_with_pieces = list(self.find_pieces(pos_coords))
        if isinstance(self.piece, Bispo):
            return verify_diagonal_till_piece(x, y, coords_with_pieces)
        elif isinstance(self.piece, Torre):
            return verify_cross_till_piece(x, y, coords_with_pieces)
        elif isinstance(self.piece, Rainha):
            return verify_diagonal_till_piece(x, y, coords_with_pieces) + verify_cross_till_piece(x, y, coords_with_pieces)
        elif isinstance(self.piece, Peao):
            return verify_Peao(pos_coords, coords_with_pieces)
        else:
            return(pos_coords)


    def find_pieces(self, coords):
        for coord in coords:
            if self.board[coord[0]][coord[1]]:
                yield coord


    def filter_by_team(self, pos_coords):
        n_coord = []
        for coord in pos_coords:
            piece = self.board[coord[0]][coord[1]]
            if piece:
                if piece.team == self.piece.team:
                    pass    
                else:
                    n_coord.append(coord) 
            else:
                n_coord.append(coord)
        return n_coord
    # end first-click


    # start second_click
    def get_second_click(self, x_mouse, y_mouse):
        i, j = self.get_coord(x_mouse, y_mouse)
        
        if [i, j] in self.pos_coords:
            self.move_piece((i,j), (self.i, self.j))
            self.erase_move(self.pos_coords+ [[self.i, self.j]])
            self.print_one_piece(self.piece, (i,j))
 #           king = find_king(self.board)
 #           verify_check(self.board, king, self.piece)
            self.team = change_team(self.team)
            
            if isinstance(self.piece, Rei) or isinstance(self.piece, Torre):
                self.block_rock() 
            
            if isinstance(self.piece, Rei) and self.rockGoing:
                if [i,j] in self.rockMove:
                    if i == 2:
                        self.board[3][j] = self.board[0][j]
                        self.board[0][j] = None
                    else:
                        self.board[5][j] = self.board[7][j]
                        self.board[7][j] = None
                        
                self.print_pieces()
        else:
            self.erase_move(self.pos_coords)            

        if j in (0, 7) and isinstance(self.piece, Peao):
            self.change_peao(i,j)
            self.print_pieces()


    def move_piece(self, new_coord, old_coord):
            self.board[old_coord[0]][old_coord[1]] = None
            self.board[new_coord[0]][new_coord[1]] = self.piece


    def erase_move(self,coords):
        for coord in coords:
            rect = pygame.Rect(coord[0]*self.lado, coord[1]*self.lado,
                 self.lado, self.lado)

            if (coord[0]+coord[1]) % 2:
                pygame.draw.rect(self.screen,(0, 0, 0), rect)
            else:
                pygame.draw.rect(self.screen,(255, 255, 255), rect)

        self.reprint_pieces(coords)


    def reprint_pieces(self, pos_coords):
        pos_coords = self.filter_coords(pos_coords)
        for coord in pos_coords:
            piece = self.board[coord[0]][coord[1]]
            if piece:
                self.print_one_piece(piece, coord)
                

    def change_peao(self, i, j):
        piece_index= int(input("'0': para rainha \n '1': para torre \n '2': para cavalo \n '3': para bispo"))
        piecesBrancas = [self.rainhab, self.torreb, self.cavalob, self.bispob]
        piecesPretas = [self.rainhap, self.torrep, self.cavalop, self.bispop]
        if self.piece.team == "brancas":
            self.board[i][j] = piecesBrancas[piece_index]
        if self.piece.team == "pretas":
            self.board[i][j] = piecesPretas[piece_index]


    def verify_rock(self):
        if self.piece.team == "brancas": 
            blockRock = self.rockb
        else:
            blockRock = self.rockp

        moves = self.verify_rock_pieces()
        for i in range(2):
            print(moves[i], blockRock[i])

            if moves[i] and blockRock[i]:
                self.pos_coords.append(moves[i])
                self.rockGoing = True
                self.rockMove = moves


# verifica se tem peça nas posições 123 e 56
    def verify_rock_pieces(self):
        left = [1,2,3]
        right = [5,6]
        movesb = [[2,7],[6,7]]
        movesp = [[2,0],[6,0]]
        
        if self.piece.team == "brancas":
            for i in left:
                if self.board[i][7] != None:
                    print(i, 7)
                    movesb[0] = 0
            for i in right:
                if self.board[i][7] != None:
                    print(i, 7)
                    movesb[1] = 0
            return movesb
        else:
            for i in left:
                if self.board[i][0] != None:
                    print(i, 0)
                    movesp[0] = 0
        
            for i in right:
                if self.board[i][0] != None:
                    print(i, 0)
                    movesp[1] = 0
            return movesp        

    def block_rock(self):
        if self.team == "brancas":
            if self.j == 4:
                self.rockb[0] = 0
                self.rockb[1] = 0

            if self.j == 0:
                self.rockb[0] = 0
            
            else:
                self.rockb[1] = 0
        else:
            if self.j == 4:
                self.rockp[0] = 0
                self.rockp[1] = 0

            if self.j == 0:
                self.rockp[0] = 0

            else:
                self.rockp[1] = 0


    def load_pieces(self):
        self.peaob = Peao("brancas", "peaob") 
        self.peaop = Peao("pretas", "peaop") 
        self.cavalob = Cavalo("brancas", "cavalob") 
        self.cavalop = Cavalo("pretas", "cavalop") 
        self.bispob = Bispo("brancas", "bispob") 
        self.bispop = Bispo("pretas", "bispop") 
        self.torreb = Torre("brancas", "torreb") 
        self.torrep = Torre("pretas", "torrep") 
        self.rainhab = Rainha("brancas", "rainhab") 
        self.rainhap = Rainha("pretas", "rainhap") 
        self.reib = Rei("brancas", "reib") 
        self.reip = Rei("pretas", "reip") 


    def pieces_on_matrix(self):
        for coluna in range(8):
            self.board[coluna][1] = self.peaop
            self.board[coluna][6] = self.peaob
        for coluna in range(0, 8, 7):
            self.board[coluna][0] = self.torrep
            self.board[coluna][7] = self.torreb
        for coluna in range(1, 7, 5):
            self.board[coluna][0] = self.cavalop
            self.board[coluna][7] = self.cavalob
        for coluna in range(2, 6, 3):
            self.board[coluna][0] = self.bispop
            self.board[coluna][7] = self.bispob
        self.board[3][0] = self.rainhap
        self.board[3][7] = self.rainhab
        self.board[4][0] = self.reip
        self.board[4][7] = self.reib


    def print_pieces(self):
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if piece:
                    self.print_one_piece(piece, (i, j))
                else:
                    rect = pygame.Rect(i*self.lado, j*self.lado,
                    self.lado, self.lado)

                    if (i+j) % 2:
                        pygame.draw.rect(self.screen,(0, 0, 0), rect)
                    else:
                        pygame.draw.rect(self.screen,(255, 255, 255), rect)


    def filter_coords(self, pos_coords):
        n_pos_coords = []
        for coords in pos_coords:
            if coords[0] > 7 or coords[0] < 0 or coords[1] > 7 or coords[1] < 0:
                n_pos_coords.append(coords)
        
        return [x for x in pos_coords if not (x in n_pos_coords)]





