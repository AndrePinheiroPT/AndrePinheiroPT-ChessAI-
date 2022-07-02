import pygame
from pygame.locals import *
from random import randint
from math import *
import os
import numpy as np

SCREEN_LENGTH = 600
SQUARE_LENTH = SCREEN_LENGTH/8

mouse_pressed = False
mouse_state = None
screen = pygame.display.set_mode((SCREEN_LENGTH , SCREEN_LENGTH ))
pygame.display.set_caption('Chess')

pygame.font.init()
font = pygame.font.SysFont('Arial', 15)

board_code = [
    [-1, -5, -2, -3, -4, -2, -5, -1],
    [-6, -6, -6, -6, -6, -6, -6, -6],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [6, 6, 6, 6, 6, 6, 6, 6],
    [1, 5, 2, 3, 4, 2, 5, 1]
]

board_pieces_surfaces = [[0 for j in range(0, 8)] for i in range(0, 8)]
board_pieces_surfaces_position = [[[0, 0] for j in range(0, 8)] for i in range(0, 8)]
piece_selected_code = None

def board():
    white = (243, 211, 160)
    brown = (152, 68, 31)
    for i in range(0, 8):
        for j in range(0, 8):
            pygame.draw.rect(screen, white if (i + j) % 2 == 0 else brown, pygame.Rect(i*SQUARE_LENTH, j*SQUARE_LENTH, SQUARE_LENTH, SQUARE_LENTH))
    for i in range(0, 8):
        for j in range(0, 8):
            if board_pieces_surfaces[j][i] == 0:
                continue
            screen.blit(board_pieces_surfaces[j][i], board_pieces_surfaces_position[j][i])
            
def piece():
    pieces = pygame.image.load('./assets/pieces.png').convert_alpha()
    pieces = pygame.transform.scale(pieces, (450, 150)).convert_alpha()
    for i in range(0, 8):
        for j in range(0, 8):
            if board_code[j][i] == 0:
                continue
            
            piece_surface = pygame.Surface((75, 75), pygame.SRCALPHA, 32).convert_alpha()
            piece_surface.blit(pieces, ((abs(board_code[j][i]) - 1)*(-75), -75 if np.sign(board_code[j][i]) > 0 else 0))
            board_pieces_surfaces[j][i] = piece_surface
            board_pieces_surfaces_position[j][i][0] = i*SQUARE_LENTH
            board_pieces_surfaces_position[j][i][1] = j*SQUARE_LENTH


def grab_piece():
    global piece_selected_code, mouse_state
    for i in range(0, 8):
        for j in range(0, 8):
            if mouse_pressed and (j*SQUARE_LENTH <= mouse_state[1] <= SQUARE_LENTH*(j + 1)) and (i*SQUARE_LENTH <= mouse_state[0] <= SQUARE_LENTH*(i + 1)) and board_code[j][i] != 0 and piece_selected_code == None:
                piece_selected_code = [j, i]

def drop_piece():
    global piece_selected_code, mouse_state
    if piece_selected_code != None:
        j = piece_selected_code[0]
        i = piece_selected_code[1]
        
        board_pieces_surfaces_position[j][i][0] += SQUARE_LENTH/2
        board_pieces_surfaces_position[j][i][1] += SQUARE_LENTH/2
        for k in range(0, 8):
            for n in range(0, 8):
                if (n*SQUARE_LENTH <= mouse_state[1] <= SQUARE_LENTH*(n + 1)) and (k*SQUARE_LENTH <= mouse_state[0] <= SQUARE_LENTH*(k + 1)):
                    if n != j or k != i:
                        if check_move([j, i], [n, k]):
                            print(f'{board_pieces_surfaces_position[j][i]} / {j} e {i} / {n} e {k}')
                            board_code[n][k] = board_code[j][i] 
                            board_code[j][i] = 0

                            board_pieces_surfaces[n][k] = board_pieces_surfaces[j][i]
                            board_pieces_surfaces[j][i] = 0

                            board_pieces_surfaces_position[n][k] = [k*SQUARE_LENTH, n*SQUARE_LENTH]
                            board_pieces_surfaces_position[j][i] = [0, 0]

                            piece_selected_code = None
                        else:
                            board_pieces_surfaces_position[j][i] = [i*SQUARE_LENTH, j*SQUARE_LENTH]
                            piece_selected_code = None

                    else: 
                        board_pieces_surfaces_position[j][i] = [i*SQUARE_LENTH, j*SQUARE_LENTH]
                        piece_selected_code = None
                

def check_move(init, end):
    init_square_code = board_code[init[0]][init[1]]
    end_square_code = board_code[end[0]][end[1]]
    if np.sign(init_square_code) != np.sign(end_square_code):
        delta_x = end[1] - init[1]
        delta_y = end[0] - init[0]

        if abs(init_square_code) == 6:
            return True
        if abs(init_square_code) == 5:
            if (abs(delta_x) == 2 and abs(delta_y) == 1) or (abs(delta_y) == 2 and abs(delta_x) == 1):
                return True
        if abs(init_square_code) == 4:
            if abs(delta_x) <= 1 and abs(delta_y) <= 1:
                return True
        if abs(init_square_code) == 3:
            if abs(delta_x) == abs(delta_y) or (abs(delta_x) == 0 or abs(delta_y) == 0):
                return True
        if abs(init_square_code) == 2:
            if abs(delta_x) == abs(delta_y):
                return True
        if abs(init_square_code) == 1:
            if abs(delta_x) == 0 or abs(delta_y) == 0:
                return True

        return False
    else:
        return False

    


piece()
clock = pygame.time.Clock()
while True:
    clock.tick(60)
    screen.fill((0, 0, 0))
    mouse_state = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pressed = False
            drop_piece()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pressed = True
            grab_piece()

    board()
    
    if mouse_pressed:
        if piece_selected_code != None:
            j = piece_selected_code[0]
            i = piece_selected_code[1]
            board_pieces_surfaces_position[j][i] = [mouse_state[0]-SQUARE_LENTH/2, mouse_state[1]-SQUARE_LENTH/2]


    pygame.display.flip()
    pygame.display.update()