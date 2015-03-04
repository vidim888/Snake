__author__ = 'Vadim'
import pygame
import time
import random
class Snake:
    def __init__(self, number, snake_list, buff, lead_x, lead_y, lead_x_change, lead_y_change, snake_length, direction, color):
        self.number = number
        self.snake_list = snake_list
        self.buff = buff
        self.lead_x = lead_x
        self.lead_y = lead_y
        self.lead_x_change = lead_x_change
        self.lead_y_change = lead_y_change
        self.snake_length = snake_length
        self.direction = direction
        self.color = color
pygame.init()
white = (255, 255, 255)
black = (0, 0, 0)
red = (155, 0, 0)
tongue_red = (255, 0, 0)
green = (0, 155, 0)
blue = (0, 0, 155)
yellow = (0, 155, 155)
display_width = 800
display_height = 600
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Snake :3')
icon = pygame.image.load('C:/Users/Vadim/Desktop/New folder/GraphicsGale/pictures of that/Icon.png')
pygame.display.set_icon(icon)
headImg = pygame.image.load('C:/Users/Vadim/Desktop/New folder/GraphicsGale/pictures of that/SnakeHead.png')
head_color = [[3, 4], [4, 4], [5, 4], [6, 4], [2, 5], [3, 5], [4, 5], [5, 5], [6, 5], [7, 5], [1, 6], [2, 6], [3, 6],
              [4, 6], [5, 6], [6, 6], [7, 6], [8, 6], [1, 7], [2, 7], [3, 7], [4, 7], [5, 7], [6, 7], [7, 7], [8, 7],
              [0, 8], [1, 8], [4, 8], [5, 8], [8, 8], [9, 8], [0, 9], [1, 9], [4, 9], [5, 9], [8, 9], [9, 9]]
head_eyes = [[2, 8], [3, 8], [6, 8], [7, 8], [2, 9], [3, 9], [6, 9], [7, 9]]
head_tongue = [[3, 0], [6, 0], [3, 1], [4, 1], [5, 1], [6, 1], [4, 2], [5, 2], [4, 3], [5, 3]]
appleImg = pygame.image.load('C:/Users/Vadim/Desktop/New folder/GraphicsGale/pictures of that/Apple.png')
block_size = 10
AppleThickness = 10
gameExit = False
lead_x = display_width/2
lead_y = display_height/2
lead_x_change = 0
lead_y_change = 0
FPS = 30
clock = pygame.time.Clock()
smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 80)
def pause():
    paused = True
    message_to_screen("Paused", black, -100, 0, size = 'large')
    message_to_screen('Press C to continue or Q to quit.', black, 25)
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        clock.tick(5)
def score(score):
    text = smallfont.render("Score: "+str(score), True, black)
    gameDisplay.blit(text, [3, 3])
def randAppleGen():
    randAppleX = round(random.randrange(0, display_width - AppleThickness)/AppleThickness)*AppleThickness
    randAppleY = round(random.randrange(0, display_height - AppleThickness)/AppleThickness)*AppleThickness
    return randAppleX, randAppleY
def gameIntro():
    intro = True
    players_number = 0
    while intro:
        gameDisplay.fill(white)
        message_to_screen("Welcome to Snake", green, -100, size='large')
        message_to_screen("The objective of the game is to eat red apples", black, -30)
        message_to_screen("The more apples you eat, the longer you get", black, 10)
        message_to_screen("If you run into yourself or the edges, you die!", black, 50)
        message_to_screen("Press C to play, P to pause, or Q to quit.", black, 180)
        message_to_screen("V to add players.", black, 210)
        message_to_screen("Players: " + str(players_number+1), black, 260, size='medium')
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    gameExit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        intro = False
                        gameExit = True
                    if event.key == pygame.K_c:
                        intro = False
                        gameLoop(players_number%4+1)
                    if event.key == pygame.K_v:
                        players_number += 1
                        players_number = players_number % 4
        pygame.display.update()
        clock.tick(FPS)
def snake(block_size, snake_list, color, direction):
    for XnY in snake_list[:-1]:
        pygame.draw.rect(gameDisplay, color, [XnY[0], XnY[1], block_size, block_size])
    if block_size == 10:
        if direction == 'right':
            for x in head_color:
                pygame.Surface.set_at(gameDisplay, (int(snake_list[-1][0] - x[1] + 9), int(snake_list[-1][1] - x[0] + 9)), color)
            for x in head_tongue:
                pygame.Surface.set_at(gameDisplay, (int(snake_list[-1][0] - x[1] + 9), int(snake_list[-1][1] - x[0] + 9)), tongue_red)
            for x in head_eyes:
                pygame.Surface.set_at(gameDisplay, (int(snake_list[-1][0] - x[1] + 9), int(snake_list[-1][1] - x[0] + 9)), black)
        elif direction == 'left':
            for x in head_color:
                pygame.Surface.set_at(gameDisplay, (int(snake_list[-1][0] + x[1]), int(snake_list[-1][1] + x[0])), color)
            for x in head_tongue:
                pygame.Surface.set_at(gameDisplay, (int(snake_list[-1][0] + x[1]), int(snake_list[-1][1] + x[0])), tongue_red)
            for x in head_eyes:
                pygame.Surface.set_at(gameDisplay, (int(snake_list[-1][0] + x[1]), int(snake_list[-1][1] + x[0])), black)
        elif direction == 'up':
            for x in head_color:
                pygame.Surface.set_at(gameDisplay, (int(snake_list[-1][0] + x[0]), int(snake_list[-1][1] + x[1])), color)
            for x in head_tongue:
                pygame.Surface.set_at(gameDisplay, (int(snake_list[-1][0] + x[0]), int(snake_list[-1][1] + x[1])), tongue_red)
            for x in head_eyes:
                pygame.Surface.set_at(gameDisplay, (int(snake_list[-1][0] + x[0]), int(snake_list[-1][1] + x[1])), black)
        elif direction == 'down':
            for x in head_color:
                pygame.Surface.set_at(gameDisplay, (int(snake_list[-1][0] - x[0] + 9), int(snake_list[-1][1] - x[1] + 9)), color)
            for x in head_tongue:
                pygame.Surface.set_at(gameDisplay, (int(snake_list[-1][0] - x[0] + 9), int(snake_list[-1][1] - x[1] + 9)), tongue_red)
            for x in head_eyes:
                pygame.Surface.set_at(gameDisplay, (int(snake_list[-1][0] - x[0] + 9), int(snake_list[-1][1] - x[1] + 9)), black)
    #else:
        #pygame.draw.rect(gameDisplay, green, [snake_list[-1][0], snake_list[-1][1], block_size, block_size])
def text_objects(text, color, size):
    if size == 'small':
        textSurface = smallfont.render(text, True, color)
    elif size == 'medium':
        textSurface = medfont.render(text, True, color)
    elif size == 'large':
        textSurface = largefont.render(text, True, color)
    return textSurface, textSurface.get_rect()
def message_to_screen(msg, color, y_displace=0, x_displace=0, size='small'):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = ((display_width / 2) + x_displace), ((display_height / 2) + y_displace)
    gameDisplay.blit(textSurf, textRect)
def make_players(players_number):
    if players_number == 1:
        first = Snake(1, [], False, display_width/2, display_height/2, 0, 0, 1, 'up', green)
        return([first])
    elif players_number == 2:
        first = Snake(1, [], False, display_width/3, display_height/2, 0, 0, 1, 'up', green)
        second = Snake(2, [], False, display_width*2/3, display_height/2, 0, 0, 1, 'up', red)
        return([first, second])
    elif players_number == 3:
        first = Snake(1, [], False, display_width/4, display_height/2, 0, 0, 1, 'up', green)
        second = Snake(2, [], False, display_width/2, display_height/2, 0, 0, 1, 'up', red)
        third = Snake(3, [], False, display_width*3/4, display_height/2, 0, 0, 1, 'up', blue)
        return([first, second, third])
    elif players_number == 4:
        first = Snake(1, [], False, display_width/5, display_height/2, 0, 0, 1, 'up', green)
        second = Snake(2, [], False, display_width*2/5, display_height/2, 0, 0, 1, 'up', red)
        third = Snake(3, [], False, display_width*3/5, display_height/2, 0, 0, 1, 'up', blue)
        fourth = Snake(4, [], False, display_width*4/5, display_height/2, 0, 0, 1, 'up', yellow)
        return([first, second, third, fourth])
def gameLoop(players_number):
    gameExit = False
    gameOver = False
    lead_x = display_width/2
    lead_y = display_height/2
    lead_x_change = 0
    lead_y_change = 0
    snake_list = []
    snake_length = 1
    list_of_players = make_players(players_number)
    randAppleX, randAppleY = randAppleGen()
    while not gameExit:
        if gameOver == True:
            gameDisplay.fill(white)
            message_to_screen("Game Over", red, -50, size='large')
            message_to_screen("Press C to Play Again or Q to Quit", black, 50, size='medium')
            score(snake_length - 1)
            pygame.display.update()
        while gameOver == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameOver = False
                    gameExit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop(players_number)
                    if event.key == pygame.K_p:
                        gameIntro()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if list_of_players[0].lead_x_change == 0:
                        list_of_players[0].direction = 'left'
                        list_of_players[0].lead_x_change = -block_size
                        list_of_players[0].lead_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    if list_of_players[0].lead_x_change == 0:
                        list_of_players[0].direction = 'right'
                        list_of_players[0].lead_x_change = block_size
                        list_of_players[0].lead_y_change = 0
                elif event.key == pygame.K_UP:
                    if list_of_players[0].lead_y_change == 0:
                        list_of_players[0].direction = 'up'
                        list_of_players[0].lead_y_change = -block_size
                        list_of_players[0].lead_x_change = 0
                elif event.key == pygame.K_DOWN:
                    if list_of_players[0].lead_y_change == 0:
                        list_of_players[0].direction = 'down'
                        list_of_players[0].lead_y_change = block_size
                        list_of_players[0].lead_x_change = 0
                elif event.key == pygame.K_p:
                    pause()
        if list_of_players[0].lead_x >= display_width or list_of_players[0].lead_x < 0 \
                or list_of_players[0].lead_y >= display_height or list_of_players[0].lead_y < 0:
            gameOver = True
            #  print(event)
        list_of_players[0].lead_x += list_of_players[0].lead_x_change
        list_of_players[0].lead_y += list_of_players[0].lead_y_change
        gameDisplay.fill(white)
        if AppleThickness == 10:
            gameDisplay.blit(appleImg, (randAppleX, randAppleY))
        else:
            pygame.draw.rect(gameDisplay, red, [randAppleX, randAppleY, AppleThickness, AppleThickness])
        for player in list_of_players:
            snakeHead = []
            snakeHead.append(player.lead_x)
            snakeHead.append(player.lead_y)
            player.snake_list.append(snakeHead)
        #snakeHead = []
        #snakeHead.append(lead_x)
        #snakeHead.append(lead_y)
        #snake_list.append(snakeHead)
        if len(list_of_players[0].snake_list) > list_of_players[0].snake_length:
            del list_of_players[0].snake_list[0]
        for eachSegment in list_of_players[0].snake_list[:-1]:
            if eachSegment == snakeHead:
                gameOver = True
        for player in list_of_players:
            snake(block_size, player.snake_list, player.color, list_of_players[0].direction)
        #snake(block_size, snake_list, green)
        score(snake_length - 1)
        pygame.display.update()
        if list_of_players[0].lead_x >= randAppleX and list_of_players[0].lead_x < randAppleX + AppleThickness \
                or list_of_players[0].lead_x + block_size > randAppleX and list_of_players[0].lead_x + block_size <= randAppleX + AppleThickness:
            if list_of_players[0].lead_y >= randAppleY and list_of_players[0].lead_y < randAppleY + AppleThickness \
                    or list_of_players[0].lead_y + block_size > randAppleY and list_of_players[0].lead_y + block_size <= randAppleY + AppleThickness:
                randAppleX, randAppleY = randAppleGen()
                list_of_players[0].snake_length += 1
        clock.tick(FPS)
    pygame.quit()
    quit()
gameIntro()