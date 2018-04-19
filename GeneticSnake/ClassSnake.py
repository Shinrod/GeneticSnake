# -*- coding: utf-8 -*-
'''
Universal Snake object
'''

### IMPORTS ###
import pygame as pg
import numpy as np
from ClassFood import Food

### CLASS ###
class Snake:
    
    def __init__(self, hiding=True, window=None, xMax=640, yMax=640, xSize=20, ySize=20):
        '''
        Initialize the snake :
            - hiding says if the snake has to be printed or not
            - xMax and yMax are the bounds of the window (Must be a multiple of xSize and ySize)
            - xSize and ySize define the size of 1 square of the grid
        '''
        ## CONSTANTS
        # Health gain each time some food is eaten
        self.cst_health = 200
        # Extend by <sizeGained> units each time he eats some food
        self.cst_sizeGained = 1
        ## SNAKE STUFF
        # The body is just the head at the begining
        # The head will always be at the index -1
        self.head = pg.Rect(320,320,xSize,ySize)
        self.body = [self.head]
        # Give a direction to the snake
        # 0 -> RIGHT, 1 -> LEFT, 2 -> UP, 3 -> DOWN        
        self.direction = 0        
        # Set the number of frame before the tail start to be erased
        self.dont_erase = 3
        # Score : Number of apple eaten so far
        self.score = 0
        # Set a boolean which says if the snake is alive
        self.alive = True
        # Time spent alive
        self.time = 0
        # Time before he dies if he doesn't eat an apple
        self.health = self.cst_health
        # Say if we see him or not
        self.hiding = hiding
        self.window = window
        # Set the window parameters
        self.xMax = xMax
        self.yMax = yMax
        self.xSize = xSize
        self.ySize = ySize
        # Give him a food to focus on
        self.food = Food(self.xMax, self.yMax, self.xSize, self.ySize)
        
        
    def erase(self):
        ''' Erases the tail of the snake '''
        # If it is allowed to erase, it earases the tail
        if self.dont_erase == 0:
            # If the snake isn't hiding, erase he's tail from the screen
            if not self.hiding:
                pg.draw.rect(self.window,(64,64,64),self.body[0])
                pg.display.flip()
            # Remove it from the body
            self.body.pop(0)                
        else :
            # Else, it decrease the 'dont_erase' counter by 1
            self.dont_erase -= 1
            
    def hit_smthg(self):
        ''' Defines what happens if the head hit something '''
        # If the head collides with the apple
        if self.head.colliderect(self.food):
            # Increase the score by 1
            self.score += 1
            # Increase he's health by <health>
            self.health += self.cst_health
            # Let the snake be taller by <sizeGained> units
            self.dont_erase += self.cst_sizeGained
            # Make a new apple
            self.food = Food(self.xMax, self.yMax, self.xSize, self.ySize)
        # If the head hits a ANOTHER part of the body
        if self.head.collidelist(self.body) != len(self.body)-1:
            # Then he dies
            self.alive = False
        # If the head hits a wall
        coord_head = list(self.head)
        if coord_head[0] >= self.xMax or coord_head[0] < 0 or coord_head[1] >= self.yMax or coord_head[1] < 0:
            # Then he dies
            self.alive = False
        # If he's health is below 0
        if self.health <= 0:
            #Then he dies
            self.alive = False
            
    def move(self):
        ''' Make the snake move in he's current direction '''
        # If the snake isn't hiding, make he's old head a bit darker
        if not self.hiding:
            pg.draw.rect(self.window,(150,255,150),self.head)
        # Make the head move
        if self.direction == 0:
            self.head = self.head.move(self.xSize,0) # Go RIGHT
        elif self.direction == 1:
            self.head = self.head.move(-self.xSize,0) # Go LEFT
        elif self.direction == 2:
            self.head = self.head.move(0,-self.ySize) # Go UP
        elif self.direction == 3:
            self.head = self.head.move(0,self.ySize) # Go DOWN
        # If the snake isn't hiding, show the new head
        if not self.hiding:
            pg.draw.rect(self.window,(200,255,200),self.head)
            self.food.show(self.window)
            pg.display.flip()
        # Add the new head to the body
        self.body.append(self.head)
        self.time += 1
        self.health -= 1
        
    def analyse(self):
        ''' Get the distance between the head and each other things '''
        # Have all the distances in each direction
        # Index : 0 to 7 -> Food distance, 8 to 15 -> Body distance, 16 to 23 -> Wall distance
        distance = np.zeros((24,))
        # Once the food is found, it can't be on an other axis. Thus this isn't changed back to false each it
        food_found = False
        # Analyse in each direction (from Right to Right-Up clockwise)
        for side in range(8):
            body_found = False
            # Make a placeholder rect
            rect = self.head
            coords = list(rect)
            # Keep track of how many tiles the rect have travelled
            travel = 0
            while coords[0] < self.xMax and coords[0] >= 0 and coords[1] < self.yMax and coords[1] >= 0:
                # Make the placeholder move
                if side == 0: # Check Right
                    rect = rect.move(self.xSize,0)
                elif side == 1: # Check Right-Down
                    rect = rect.move(self.xSize,self.ySize)
                elif side == 2: # Check Down
                    rect = rect.move(0,self.ySize)
                elif side == 3: # Check Left-Down
                    rect = rect.move(-self.xSize,self.ySize)    
                elif side == 4: # Check Left
                    rect = rect.move(-self.xSize,0)
                elif side == 5: # Check Left-Up
                    rect = rect.move(-self.xSize,-self.ySize)
                elif side == 6: # Check Up
                    rect = rect.move(0,-self.ySize)
                elif side == 7: # Check Right-Up
                    rect = rect.move(self.xSize,-self.ySize)
                # Increase the step counter by 1
                travel += 1
                # Get the new coords
                coords = list(rect)
                # Check if it collides with some food
                if rect.colliderect(self.food) and not(food_found):
                    distance[side] = travel
                    food_found = True
                # Check if it collides with it's own body
                index_collision = rect.collidelist(self.body)
                if index_collision != len(self.body)-1 and index_collision != -1 and not(body_found):
                    distance[side+8] = travel
                    body_found = True
            # If 'while' is over, it means that the placeholder has hit a wall
            distance[side+16] = travel
        # Give the informations to the brain !
        return distance