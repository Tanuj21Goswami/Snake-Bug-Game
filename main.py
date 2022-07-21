from re import L
import pygame
import time
from pygame.locals import *
import random

SIZE=15

class Insect:
    def __init__(self,parent_screen) :
        self.image =pygame.image.load('insect.jpg')
        self.parent_screen=parent_screen
        self.x=SIZE*3
        self.y=SIZE*3

    def draw(self):
        self.parent_screen.blit(self.image,(self.x,self.y))
        pygame.display.update()
    
    def move(self):
        self.x = random.randint(1,65)*SIZE
        self.y = random.randint(1,32)*SIZE

    

class Snake:
    def __init__(self,parent_screen,length):
        self.length=length
        self.parent_screen =parent_screen
        self.block =pygame.image.load('block.jpg')
        self.x=[SIZE]*length
        self.y=[SIZE]*length
        self.direction='down'
    
    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)
    
    def draw(self):
        # self.parent_screen.fill((79, 83, 115))
        for i in range(self.length):
            self.parent_screen.blit(self.block,(self.x[i],self.y[i]))
        pygame.display.update()
    

    def walk(self):
        for i in range(self.length-1,0,-1):
            self.x[i]=self.x[i-1]
            self.y[i]=self.y[i-1]

        if self.direction=='up':
            self.y[0]-=SIZE
        if self.direction=='down':
            self.y[0]+=SIZE
        if self.direction=='right':
            self.x[0]+=SIZE
        if self.direction=='left':
            self.x[0]-=SIZE
        
        self.draw()

    def move_left(self):
        self.direction='left'
    def move_right(self):
        self.direction='right' 
    def move_up(self):
        self.direction='up'
    def move_down(self):
        self.direction='down'

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake and Insect Game")

        pygame.mixer.init()
        self.play_background_music()

        self.surface=pygame.display.set_mode((1000,500))
        self.surface.fill((79, 83, 115))
        self.snake=Snake(self.surface,1)
        self.snake.draw()
        self.insect=Insect(self.surface)
        self.insect.draw()


    def is_collision(self,x1,y1,x2,y2):
        if x1>=x2 and x1<x2+SIZE:
            if y1>=y2 and y1<y2+SIZE:
                return True

        return False

    def render_background(self):
        bg = pygame.image.load('backround.jpg')
        self.surface.blit(bg, (0,0))

    def play_background_music(self):
        pygame.mixer.music.load('background_music.mp3')
        pygame.mixer.music.play(-1, 0)

    def play(self):
        self.render_background()
        self.snake.walk()
        self.insect.draw()
        self.display_score()
        pygame.display.update()

        # Snake colliding with insect
        if self.is_collision(self.snake.x[0],self.snake.y[0],self.insect.x,self.insect.y):
            # print("Collision ")
            sound=pygame.mixer.Sound('ding.mp3')
            pygame.mixer.Sound.play(sound)
            self.snake.increase_length()
            self.insect.move()
        
        # Snake colliding with itself
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                sound=pygame.mixer.Sound('crash.mp3')
                pygame.mixer.Sound.play(sound)
                raise "Game over"
                # print("game over")
                # exit(0)
                # self.play_sound('crash')
                # raise "Collision Occurred"
        
        # snake colliding with the boundries of the window
        if not (0 <= self.snake.x[0] <= 1000 and 0 <= self.snake.y[0] <= 800):
            sound=pygame.mixer.Sound('crash.mp3')
            pygame.mixer.Sound.play(sound)
            raise "Boundary Error"


    def display_score(self):
        font = pygame.font.SysFont('verdana',30)
        score = font.render(f"Score: {self.snake.length*10}",True,(204, 35, 74))
        self.surface.blit(score,(750,10))

    def show_game_over(self):
        self.render_background()
        self.surface.fill((79, 83, 115))
        font = pygame.font.SysFont('verdana',30)
        line1=font.render(f"Game is Over!! Your Score is {self.snake.length*10}",True,(204, 35, 74))
        self.surface.blit(line1,(220,200))
        line2 = font.render("To play again press Enter. To exit press Escape!", True, (255, 255, 255))
        self.surface.blit(line2,(150,250))
        pygame.mixer.music.pause()
        pygame.display.flip()

    def reset(self):
        self.snake = Snake(self.surface,1)
        self.apple = Insect(self.surface)

    def run(self):
        running=True
        pause=False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running=False
                    
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause=False
                    
                    if not pause:
                        if event.key==K_UP:
                            self.snake.move_up()
                        if event.key==K_DOWN:
                            self.snake.move_down()
                        if event.key==K_LEFT:
                            self.snake.move_left()
                        if event.key==K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running=False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause=True
                self.reset()

            
            time.sleep(0.2)
        


if __name__=="__main__" :
    game=Game()
    game.run()
