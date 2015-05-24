__author__ = 'Vadim'
import pygame
import time
import random
class Snake:
    def __init__(self, number, lead_x, lead_y, color):
        self.number = number
        self.snake_list = []
        self.buff = [0, 0, 0, 0]
        self.lead_x = lead_x
        self.lead_y = lead_y
        self.lead_x_change = 0
        self.lead_y_change = -10
        self.snake_length = 1
        self.score_per_apple = 1
        self.direction = 'up'
        self.color = color
        self.apple_x = 0
        self.apple_y = 0
        self.AppleThickness = 10
        self.death = False
        self.immortality = False
pygame.init()
white = (255, 255, 255)
black = (0, 0, 0)
red = (155, 0, 0)
tongue_red = (255, 0, 0)
green = (0, 155, 0)
leaf_green = (0, 255, 0)
blue = (0, 0, 155)
yellow = (155, 155, 0)
buff_apple_colors = [red, green, blue, yellow]
icon = pygame.image.load('Icon.png')
pygame.display.set_icon(icon)
display_width = 800
display_height = 600
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Snake :3')
# headImg = pygame.image.load('C:/Users/Vadim/Desktop/New folder/GraphicsGale/pictures of that/SnakeHead.png')
head_color = [[3, 4], [4, 4], [5, 4], [6, 4], [2, 5], [3, 5], [4, 5], [5, 5], [6, 5], [7, 5], [1, 6], [2, 6], [3, 6],
              [4, 6], [5, 6], [6, 6], [7, 6], [8, 6], [1, 7], [2, 7], [3, 7], [4, 7], [5, 7], [6, 7], [7, 7], [8, 7],
              [0, 8], [1, 8], [4, 8], [5, 8], [8, 8], [9, 8], [0, 9], [1, 9], [4, 9], [5, 9], [8, 9], [9, 9]]
head_eyes = [[2, 8], [3, 8], [6, 8], [7, 8], [2, 9], [3, 9], [6, 9], [7, 9]]
head_tongue = [[3, 0], [6, 0], [3, 1], [4, 1], [5, 1], [6, 1], [4, 2], [5, 2], [4, 3], [5, 3]]
apple_color = [[2, 3], [3, 3], [6, 3], [7, 3], [1, 4], [2, 4], [3, 4], [4, 4], [5, 4], [6, 4], [7, 4], [8, 4], [0, 5],
               [1, 5], [2, 5], [3, 5], [4, 5], [5, 5], [6, 5], [7, 5], [8, 5], [9, 5], [0, 6], [1, 6], [2, 6], [3, 6],
               [4, 6], [5, 6], [6, 6], [7, 6], [8, 6], [9, 6], [0, 7], [1, 7], [2, 7], [3, 7], [4, 7], [5, 7], [6, 7],
               [7, 7], [8, 7], [9, 7], [1, 8], [2, 8], [3, 8], [4, 8], [5, 8], [6, 8], [7, 8], [8, 8], [2, 9], [3, 9],
               [6, 9], [7, 9]]
apple_leaf = [[1, 0], [2, 0], [7, 0], [1, 1], [2, 1], [3, 1], [6, 1], [7, 1], [8, 1], [2, 2], [3, 2], [4, 2], [5, 2],
              [6, 2], [7, 2], [4, 3], [5, 3]]
apple_black = [[4, 9], [5, 9]]
buff_list = ["slow: ", "score x2: ", "apple x2: ", "immortality: "]
# appleImg = pygame.image.load('C:/Users/Vadim/Desktop/New folder/GraphicsGale/pictures of that/Apple.png')
block_size = 10
AppleThickness = 10
map_dying_coefficient = 10
dead_blocks_number = 10
gameExit = False
FPS = 30
frames_buff_works = 2000
chance_of_buff_apple = 1000  # chance is c/1000
clock = pygame.time.Clock()
verysmallfont = pygame.font.SysFont("comicsansms", 10)
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
        clock.tick(FPS)
def score(score, player_number, color):
    text = smallfont.render("Score: "+str(score), True, color)
    gameDisplay.blit(text, [200*(player_number - 1) + 50, 3])
def buff_draw(number, color, buff):
    for buff_number, quantity in enumerate(buff):
        text = pygame.font.SysFont("comicsansms", 17).render(buff_list[buff_number] + str(quantity), True, color)
        gameDisplay.blit(text, [200*(number - 1) + 50, 30 + buff_number*20])
def randAppleGen():
    found = False
    while not found:
        randAppleX = round(random.randrange(AppleThickness, display_width - 2*AppleThickness)/AppleThickness)*AppleThickness
        randAppleY = round(random.randrange(AppleThickness, display_height - 2*AppleThickness)/AppleThickness)*AppleThickness
        if pygame.Surface.get_at(gameDisplay, (int(randAppleX + 5), int(randAppleY + 5))) != black and \
                        pygame.Surface.get_at(gameDisplay, (int(randAppleX + 5), int(randAppleY + 5))) != green and \
                        pygame.Surface.get_at(gameDisplay, (int(randAppleX + 5), int(randAppleY + 5))) != red and \
                        pygame.Surface.get_at(gameDisplay, (int(randAppleX + 5), int(randAppleY + 5))) != yellow and \
                        pygame.Surface.get_at(gameDisplay, (int(randAppleX + 5), int(randAppleY + 5))) != blue:
            found = True
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
        message_to_screen("created by: Vadim Shved", black, 290, 340, 'verysmall')
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
    else:
        pygame.draw.rect(gameDisplay, green, [snake_list[-1][0], snake_list[-1][1], block_size, block_size])
def apple_draw(apple_x, apple_y, color, size):
    if size == 10:
        for x in apple_color:
            pygame.Surface.set_at(gameDisplay, (int(apple_x + x[0]), int(apple_y + x[1])), color)
        for x in apple_black:
            pygame.Surface.set_at(gameDisplay, (int(apple_x + x[0]), int(apple_y + x[1])), black)
        for x in apple_leaf:
            pygame.Surface.set_at(gameDisplay, (int(apple_x + x[0]), int(apple_y + x[1])), leaf_green)
    elif size % 10 == 0:
        k = int(size/10)
        for x in apple_color:
            pygame.Surface.set_at(gameDisplay, (int(apple_x + k*x[0]), int(apple_y + k*x[1])), color)
            pygame.Surface.set_at(gameDisplay, (int(apple_x + k*x[0] + 1), int(apple_y + k*x[1])), color)
            pygame.Surface.set_at(gameDisplay, (int(apple_x + k*x[0]), int(apple_y + k*x[1] + 1)), color)
            pygame.Surface.set_at(gameDisplay, (int(apple_x + k*x[0] + 1), int(apple_y + k*x[1] + 1)), color)
        for x in apple_black:
            pygame.Surface.set_at(gameDisplay, (int(apple_x + k*x[0]), int(apple_y + k*x[1])), black)
            pygame.Surface.set_at(gameDisplay, (int(apple_x + k*x[0] + 1), int(apple_y + k*x[1])), black)
            pygame.Surface.set_at(gameDisplay, (int(apple_x + k*x[0]), int(apple_y + k*x[1] + 1)), black)
            pygame.Surface.set_at(gameDisplay, (int(apple_x + k*x[0] + 1), int(apple_y + k*x[1] + 1)), black)
        for x in apple_leaf:
            pygame.Surface.set_at(gameDisplay, (int(apple_x + k*x[0]), int(apple_y + k*x[1])), leaf_green)
            pygame.Surface.set_at(gameDisplay, (int(apple_x + k*x[0] + 1), int(apple_y + k*x[1])), leaf_green)
            pygame.Surface.set_at(gameDisplay, (int(apple_x + k*x[0]), int(apple_y + k*x[1] + 1)), leaf_green)
            pygame.Surface.set_at(gameDisplay, (int(apple_x + k*x[0] + 1), int(apple_y + k*x[1] + 1)), leaf_green)
    else:
        pygame.draw.rect(gameDisplay, red, [randAppleX, randAppleY, size, size])
def text_objects(text, color, size):
    if size == 'verysmall':
        textSurface = verysmallfont.render(text, True, color)
    elif size == 'small':
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
def make_blocks():
    all_blocks = []
    block_coefficient = []
    for y in range(-1, int(display_height/10)+1):
        for x in range(-1, int(display_width/10)+1):
            block = [x*10, y*10]
            all_blocks.append(block)
            block_coefficient.append(0)
    return all_blocks, block_coefficient
def block_black(all_blocks, block_coefficient, snakeHead, dead_blocks):
    indexx = all_blocks.index(snakeHead)
    block_coefficient[indexx] += map_dying_coefficient
    if block_coefficient[indexx] >= 255:
        dead_blocks.append(all_blocks[indexx])
def draw_blocks(all_blocks, blocks_coefficients, dead_blocks):
    for coefficient, every_block in zip(blocks_coefficients, all_blocks):
        if coefficient >= 255:
            pygame.draw.rect(gameDisplay, (0, 0, 0), [every_block[0], every_block[1], 10, 10])
        else:
            pygame.draw.rect(gameDisplay, (255, 255 - coefficient, 255), [every_block[0], every_block[1], 10, 10])
    for every_block in dead_blocks:
        pygame.draw.rect(gameDisplay, (0, 0, 0), [every_block[0], every_block[1], 10, 10])
def make_players(players_number):
    if players_number == 1:
        first = Snake(1, display_width/2-((display_width/2)%block_size), display_height/2, green)
        return([first])
    elif players_number == 2:
        first = Snake(1, (display_width/3)-((display_width/3)%block_size), display_height/2, green)
        second = Snake(2, (display_width*2/3)-((display_width*2/3)%block_size), display_height/2, red)
        return([first, second])
    elif players_number == 3:
        first = Snake(1, display_width/4-((display_width/4)%block_size), display_height/2, green)
        second = Snake(2, display_width/2-((display_width/2)%block_size), display_height/2, red)
        third = Snake(3, display_width*3/4-((display_width*3/4)%block_size), display_height/2, blue)
        return([first, second, third])
    elif players_number == 4:
        first = Snake(1, display_width/5-((display_width/5)%block_size), display_height/2, green)
        second = Snake(2, display_width*2/5-((display_width*2/5)%block_size), display_height/2, red)
        third = Snake(3, display_width*3/5-((display_width*3/5)%block_size), display_height/2, blue)
        fourth = Snake(4, display_width*4/5-((display_width*4/5)%block_size), display_height/2, yellow)
        return([first, second, third, fourth])
def death_check(list_of_players):
    if len(list_of_players) == 1:
        if list_of_players[0].death:
            return(True)
        else:
            return(False)
    elif len(list_of_players) == 2:
        if list_of_players[0].death and list_of_players[1].death:
            return(True)
        else:
            return(False)
    elif len(list_of_players) == 3:
        if list_of_players[0].death and list_of_players[1].death and list_of_players[2].death:
            return(True)
        else:
            return(False)
    elif len(list_of_players) == 4:
        if list_of_players[0].death and list_of_players[1].death and list_of_players[2].death and list_of_players[3].death:
            return(True)
        else:
            return(False)
def controls(list_of_players):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if list_of_players[0].death == False:
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
            if len(list_of_players) >= 2:
                if list_of_players[1].death == False:
                    if event.key == pygame.K_a:
                        if list_of_players[1].lead_x_change == 0:
                            list_of_players[1].direction = 'left'
                            list_of_players[1].lead_x_change = -block_size
                            list_of_players[1].lead_y_change = 0
                    elif event.key == pygame.K_d:
                        if list_of_players[1].lead_x_change == 0:
                            list_of_players[1].direction = 'right'
                            list_of_players[1].lead_x_change = block_size
                            list_of_players[1].lead_y_change = 0
                    elif event.key == pygame.K_w:
                        if list_of_players[1].lead_y_change == 0:
                            list_of_players[1].direction = 'up'
                            list_of_players[1].lead_y_change = -block_size
                            list_of_players[1].lead_x_change = 0
                    elif event.key == pygame.K_s:
                        if list_of_players[1].lead_y_change == 0:
                            list_of_players[1].direction = 'down'
                            list_of_players[1].lead_y_change = block_size
                            list_of_players[1].lead_x_change = 0
            if len(list_of_players) >= 3:
                if list_of_players[2].death == False:
                    if event.key == pygame.K_g:
                        if list_of_players[2].lead_x_change == 0:
                            list_of_players[2].direction = 'left'
                            list_of_players[2].lead_x_change = -block_size
                            list_of_players[2].lead_y_change = 0
                    elif event.key == pygame.K_j:
                        if list_of_players[2].lead_x_change == 0:
                            list_of_players[2].direction = 'right'
                            list_of_players[2].lead_x_change = block_size
                            list_of_players[2].lead_y_change = 0
                    elif event.key == pygame.K_y:
                        if list_of_players[2].lead_y_change == 0:
                            list_of_players[2].direction = 'up'
                            list_of_players[2].lead_y_change = -block_size
                            list_of_players[2].lead_x_change = 0
                    elif event.key == pygame.K_h:
                        if list_of_players[2].lead_y_change == 0:
                            list_of_players[2].direction = 'down'
                            list_of_players[2].lead_y_change = block_size
                            list_of_players[2].lead_x_change = 0
            if len(list_of_players) >= 4:
                if list_of_players[3].death == False:
                    if event.key == pygame.K_k:
                        if list_of_players[3].lead_x_change == 0:
                            list_of_players[3].direction = 'left'
                            list_of_players[3].lead_x_change = -block_size
                            list_of_players[3].lead_y_change = 0
                    elif event.key == pygame.K_SEMICOLON:
                        if list_of_players[3].lead_x_change == 0:
                            list_of_players[3].direction = 'right'
                            list_of_players[3].lead_x_change = block_size
                            list_of_players[3].lead_y_change = 0
                    elif event.key == pygame.K_o:
                        if list_of_players[3].lead_y_change == 0:
                            list_of_players[3].direction = 'up'
                            list_of_players[3].lead_y_change = -block_size
                            list_of_players[3].lead_x_change = 0
                    elif event.key == pygame.K_l:
                        if list_of_players[3].lead_y_change == 0:
                            list_of_players[3].direction = 'down'
                            list_of_players[3].lead_y_change = block_size
                            list_of_players[3].lead_x_change = 0
            if event.key == pygame.K_p:
                pause()
def player_loop(list_of_players, dead_blocks, all_blocks, block_coefficient, buff_apple_x, buff_apple_y, buff_apple):
    for player in list_of_players:
        if player.buff[0] % 2 == 0:
            if player.lead_x >= display_width or player.lead_x < 0 \
                    or player.lead_y >= display_height or player.lead_y < 0:
                player.death = True
            player.lead_x += player.lead_x_change
            player.lead_y += player.lead_y_change
            if len(player.snake_list) > player.snake_length:
                del player.snake_list[0]
            if player.death == False:
                snakeHead = []
                snakeHead.append(player.lead_x)
                snakeHead.append(player.lead_y)
                player.snake_list.append(snakeHead)
                for every_block in dead_blocks:
                    if player.lead_x == every_block[0] and player.lead_y == every_block[1]:
                        if player.immortality == False:
                            player.death = True
                block_black(all_blocks, block_coefficient, snakeHead, dead_blocks)
                for all_players in list_of_players:
                    for eachSegment in all_players.snake_list[:-1]:
                        if eachSegment == snakeHead:
                            if player.immortality == False:
                                player.death = True
                    if all_players.death:
                        if player.lead_x >= all_players.apple_x and player.lead_x < all_players.apple_x + all_players.AppleThickness or\
                                                        player.lead_x + block_size > all_players.apple_x and player.lead_x + block_size <= all_players.apple_x + AppleThickness:
                            if player.lead_y >= all_players.apple_y and player.lead_y < all_players.apple_y + all_players.AppleThickness or\
                                                            player.lead_y + block_size > all_players.apple_y and player.lead_y + block_size <= all_players.apple_y + AppleThickness:
                                if player.immortality == False:
                                    player.death = True
            if player.death == True:
                player.lead_x_change = 0
                player.lead_y_change = 0
                player.color = black
            if player.lead_x >= player.apple_x and player.lead_x < player.apple_x + player.AppleThickness \
                    or player.lead_x + block_size > player.apple_x and player.lead_x + block_size <= player.apple_x + player.AppleThickness:
                if player.lead_y >= player.apple_y and player.lead_y < player.apple_y + player.AppleThickness \
                        or player.lead_y + block_size > player.apple_y and player.lead_y + block_size <= player.apple_y + player.AppleThickness:
                    player.apple_x, player.apple_y = randAppleGen()
                    player.snake_length += player.score_per_apple
            if buff_apple == True:
                if player.lead_x >= buff_apple_x and player.lead_x < buff_apple_x + AppleThickness \
                        or player.lead_x + block_size > buff_apple_x and player.lead_x + block_size <= buff_apple_x + AppleThickness:
                    if player.lead_y >= buff_apple_y and player.lead_y < buff_apple_y + AppleThickness \
                            or player.lead_y + block_size > buff_apple_y and player.lead_y + block_size <= buff_apple_y + AppleThickness:
                        buff_apple = False
                        buff_number = random.randint(1, 4)
                        if buff_number == 1:
                            player.buff[buff_number-1] += int(frames_buff_works*0.4)
                        elif buff_number == 2:
                            player.buff[buff_number-1] += int(frames_buff_works)
                            player.score_per_apple = 2
                        elif buff_number == 3:
                            player.buff[buff_number-1] += int(frames_buff_works*0.5)
                            player.AppleThickness = AppleThickness*2
                        elif buff_number == 4:
                            player.buff[buff_number-1] += int(frames_buff_works*0.2)
                            player.immortality = True
        for number, buff_time in enumerate(player.buff):
                if buff_time >= 1:
                    player.buff[number] -= 1
                    if player.buff[number] == 0:
                        if number == 0:
                            pass
                        elif number == 1:
                            player.score_per_apple = 1
                        elif number == 2:
                            player.AppleThickness = AppleThickness
                        elif number == 3:
                            player.immortality = False
        score(player.snake_length - 1, player.number, player.color)
        buff_draw(player.number, player.color, player.buff)
        apple_draw(player.apple_x, player.apple_y, player.color, player.AppleThickness)
        snake(block_size, player.snake_list, player.color, player.direction)
        return buff_apple
def gameLoop(players_number):
    gameExit = False
    gameOver = False
    list_of_players = make_players(players_number)
    all_blocks, block_coefficient = make_blocks()
    dead_blocks = []
    buff_apple = False
    buff_apple_color_number = 0
    for block in range(dead_blocks_number):
        block_x = 10*random.randint(0, int(display_width/10))
        block_y = 10*random.randint(0, int(display_height/10))
        block = [block_x, block_y]
        dead_blocks.append(block)
    for player in list_of_players:
        player.apple_x, player.apple_y = randAppleGen()
    while not gameExit:
        if gameOver == True:
            # gameDisplay.fill(white)
            message_to_screen("Game Over", red, -50, size='large')
            message_to_screen("Press C to Play Again or Q to Quit", black, 50, size='medium')
            finish_score = []
            for player in list_of_players:
                x = player.snake_length - 1
                finish_score.append(x)
            y = max(finish_score)
            message_to_screen("Player with " + str(y) + " points has won!", black, 150)
            for player in list_of_players:
                score(player.snake_length - 1, player.number, player.color)
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
        controls(list_of_players)
        if buff_apple == False:
            buff_apple_x = -100
            buff_apple_y = -100
            random_number = random.randint(chance_of_buff_apple, 1000)
            if random_number == 1000:
                buff_apple = True
                buff_apple_x, buff_apple_y = randAppleGen()
        gameDisplay.fill(white)
        draw_blocks(all_blocks, block_coefficient, dead_blocks)  # Draw after this!
        if buff_apple == True:
            buff_apple_color_number += 1
            apple_draw(buff_apple_x, buff_apple_y, buff_apple_colors[buff_apple_color_number % 4], AppleThickness)
        buff_apple = player_loop(list_of_players, dead_blocks, all_blocks, block_coefficient, buff_apple_x, buff_apple_y, buff_apple)
        gameOver = death_check(list_of_players)
        pygame.display.update()
        clock.tick(FPS)
    pygame.quit()
    quit()
gameIntro()