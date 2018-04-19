# -*- coding: utf-8 -*-
'''
Food object for the Universal Snake
'''

### IMPORTS ###
import pygame as pg
import numpy as np

### CLASS ###
class Food:
    
    def __init__(self, xMax=640, yMax=640, xSize=20, ySize=20):
        '''
        Makes an apple for the snake to eat
        xMax : The max width
        yMax : The max height
        xSize : The x size of 1 rectangle
        ySize : The y size of 1 rectangle
        '''
        # Draw a random square on the grid
        x = np.random.randint(0,xMax/xSize)
        y = np.random.randint(0,yMax/ySize)
        # Have the coords of this square
        x = x*xSize
        y = y*ySize
        # Have a Rect object to work with
        self.rect = pg.Rect(x,y,xSize,ySize)
        
    def show(self,window):
        ''' Show the apple onto the screen when the snake is showing off '''
        self.rect = pg.draw.rect(window,(255,0,0),self.rect)
        # Update the screen
        pg.display.flip()