import pygame
from pygame.locals import *
from random import randint
from math import *
import os

SCREEN_LENGTH = 600
SQUARE_LENTH = SCREEN_LENGTH/8

screen = pygame.display.set_mode((SCREEN_LENGTH , SCREEN_LENGTH ))
pygame.display.set_caption('Chess')

pygame.font.init()
font = pygame.font.SysFont('Arial', 15)

board_code = [
    [-1, -2, -3, -4, -5, -3, -2, -1],
    [-6, -6, -6, -6, -6, -6, -6, -6],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [6, 6, 6, 6, 6, 6, 6, 6],
    [1, 2, 3, 4, 5, 3, 2, 1]
]

def board():
    white = (243, 211, 160)
    brown = (152, 68, 31)
    for i in range(0, 8):
        for j in range(0, 8):
            pygame.draw.rect(screen, white if (i + j) % 2 == 0 else brown, pygame.Rect(i*SQUARE_LENTH, j*SQUARE_LENTH, SQUARE_LENTH, SQUARE_LENTH))
            
def piece():
    for i in range(0, 8):
        for j in range(0, 8):
            piece_code = board_code[j][i] 
            if piece_code == 0:
                continue 
            pieces = pygame.image.load('./assets/pieces.png')
            pieces = pygame.transform.scale(pieces, (450, 150))
            piece_surface = pygame.Surface((75, 75))

# draw/blit the original image on to the new surface
# in this example the original image is moved 250 pixels left and 250 pixels up
# so the crop would be a 100 x 100 image that starts at position 250,250 on the original image
            piece_surface.blit(pieces, (0, 0))
            screen.blit(piece_surface, (j, i))


clock = pygame.time.Clock()
while True:
    clock.tick(60)
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

    board()
    piece()

    pygame.display.flip()
    pygame.display.update()