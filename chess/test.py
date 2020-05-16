from piece import Rainha, Torre, Rei, Cavalo
import pygame

rainha = Rainha("brancas", "rainhab")
torre = Torre("brancas", "torreb")
rei = Rei("pretas", "reip")
cavalo = Cavalo("pretas", "cavalop")

print(cavalo.show_move(7,6))