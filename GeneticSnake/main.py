# -*- coding: utf-8 -*-

''' 
KEYCONTROL

# Game Controls #
H : Hide or show the snake
F : Accelerate the snake (can also use the + key on the keypad)
S : Decelerate the snake (can also use the - key on the keypad)

# Genetic #
E : Toggle Evolution
B : Show the best of each gen
N : New game with the best of the current gen
'''


### IMPORTS ###
from ClassInterface import Interface
import pygame as pg

### SETUP ###
pg.init()
Inter = Interface()


### THE SCRIPT ###
if __name__ == '__main__' :
    Inter.run()
    # End this
    print('Leaving...')
    pg.display.quit()











