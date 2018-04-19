# -*- coding: utf-8 -*-
''' Interface class for the Snake '''

### IMPORTS ###
import pygame as pg
from ClassSnake import Snake
from ClassGeneration import Generation

### SETUP ###
pg.init()
# Consider a key held as multiple keydown
pg.key.set_repeat(100,100)

### CLASS ###
class Interface:
    
    def __init__(self):
        ''' Initialize all the stuff '''
        # Window
        self.xMax = 640
        self.yMax = 640
        self.window = pg.display.set_mode((self.xMax,self.yMax))
        # Square size
        self.xSize = 20
        self.ySize = 20
        # Interface management
        self.list_event = []
        # Game config
        self.hiding = True
        self.running = True                     # The variable managing the infinite loop
        # Game management
        self.idle = 30                          # Time it waits before playing the next turn
        self.snake = Snake()
        # Genetic Setup
        self.gen = Generation(500, self.fitnessFunction)
        self.showBestAtEachGen = True
        print('Interface - Init complete !')


    def getEvent(self):
        '''
        Get the event from the keyboard of the user
        Read 'KEYCONTROL' for more informations
        '''
        # Update the list with the new key pressed
        self.list_event.extend(pg.event.get())
        # Go through the list of events
        for i in range(len(self.list_event)):
            event = self.list_event.pop(0)
            # Close the window when the user clicks on the red cross
            if event.type == pg.QUIT:
                self.running = False
                break
            # If the event is a keypress
            elif event.type == pg.KEYDOWN:
                # N : Start a new game (The best one the the current gen is playing)
                if event.key == pg.K_n:
                    print('\n' + 'Showing the current best...')
                    self.play(self.gen.best, True)
                # F or + : Speed up by 5
                elif event.key == pg.K_f or event.key == pg.K_KP_PLUS:
                    self.idle = self.idle - 5
                    if self.idle < 0:
                        self.idle =0
                    print('Current idle :', self.idle)
                # S or - : Slow down by 5
                elif event.key == pg.K_s or event.key == pg.K_KP_MINUS:
                    self.idle = self.idle + 5
                    print('Current idle :', self.idle)
                # H : Toggle 'hiding'
                elif event.key == pg.K_h:
                    self.hiding = not self.hiding
                    print('Hiding the snake : ', self.hiding)
                # B : Toggle 'showBestAtEachGen'
                elif event.key == pg.K_b:
                    self.showBestAtEachGen = not self.showBestAtEachGen
                # E : Launch Evolution
                elif event.key == pg.K_e:
                        self.idle = 20
                        print('Launching genetic algorithm')
                        print('Number of gen : ', end ='')
                        number_of_gen = int(self.getText())
                        self.evolution(number_of_gen)
                        print('Done !')
                        self.run()
                        
    def play(self, net, forced_to_be_seen = False):
        '''
        Let a net play a game
        '''
        if forced_to_be_seen:
            # Hold the old value of hiding in a variable
            hiding = self.hiding
            self.hiding = False
        if not self.hiding :
            # Have a grey window
            self.window.fill((64,64,64))
        # Get a snake
        self.snake = Snake(self.hiding, self.window, self.xMax, self.yMax, self.xSize, self.ySize)
        while self.snake.alive and self.running:
            self.getEvent()
            self.snake.direction = self.AIDirection(net)
            self.snake.move()
            self.snake.hit_smthg()
            if not self.hiding:
                pg.time.delay(self.idle)
            if self.snake.alive:
                self.snake.erase()
        if forced_to_be_seen:
            # Put self.hiding back at it's original state
            self.hiding = hiding
        
        
    def AIDirection(self, net):
        ''' Get the desired direction from the NeuralNet '''
        inputs = self.snake.analyse()
        outputs = net.feedforward(inputs)
        direction = outputs.index(max(outputs))
        return direction        
            
    
    def evolution(self, number_of_gen):
        '''
        Let the Genetic algorithm do it's job for <numer_of_gen> generations
        '''
        i = 0
        while i < number_of_gen and self.running:
            print('----------', 'Current gen : ', self.gen.num_gen+1, '----------')
            self.getEvent()
            self.gen.step()
            if self.showBestAtEachGen:
                print('Here is the current best ! \n')
                self.play(self.gen.best, True)
            i += 1

    def run(self):
        ''' Wait for a new command '''
        while self.running:
            self.getEvent()
            
    ## TOOLS ##
    def getText(self):
        ''' Get some text from the user '''
        text_running = True
        text = ''
        while text_running and self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN or event.key == pg.K_KP_ENTER:
                        text_running = False
                        break
                    elif event.key == pg.K_BACKSPACE:
                        text = text[:-1]
                        print('\n' + ':' , text, end='')
                    else:
                        text += event.unicode
                        print(event.unicode, end='')
        print('\n' + 'Done')
        return text
    
    
    ## GENETIC STUFF ##
    def fitnessFunction(self, net):
        '''
        Let the Net play a game and return the fitness
        '''
        self.play(net)
        # Compute fitness
        if self.snake.score <= 6:
            fitness = ((self.snake.time)**2)*2**(self.snake.score*4)
        else:
            fitness = ((self.snake.time)**2)*2**(6*4)*(self.snake.score-6)
        return fitness
