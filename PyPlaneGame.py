import random
import sys
import pygame
import time
from pygame.locals import *

window_width = 600
window_height = 499
  
window = pygame.display.set_mode((window_width, window_height))
elevation = window_height * 0.8
game_images = {}

framepersecond = 32

start_image = 'images/start.png'
obstacle_image = 'images/obstacle.png'
background_image = 'images/background.png'
planeplayer_image = 'images/player.png'
land_image = 'images/land.png'
game_over = 'images/gameover.png'

def flappygame():
    your_score = 0
    horizontal = int(window_width/5)
    vertical = int(window_width/2)
    ground = 0
    mytempheight = 100
  
    first_obstacle = createobstacle()
    second_obstacle = createobstacle()
  
    down_obstacles = [
        {'x': window_width+300-mytempheight,
         'y': first_obstacle[1]['y']},
        {'x': window_width+300-mytempheight+(window_width/2),
         'y': second_obstacle[1]['y']},
    ]
  
    up_obstacles = [
        {'x': window_width+300-mytempheight,
         'y': first_obstacle[0]['y']},
        {'x': window_width+200-mytempheight+(window_width/2),
         'y': second_obstacle[0]['y']},
    ]
  
    obstacleVelX = -4
  
    plane_velocity_y = -9
    plane_Max_Vel_Y = 10
    plane_Min_Vel_Y = -8
    planeAccY = 1
  
    plane_flap_velocity = -8
    plane_flapped = False
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if vertical > 0:
                    plane_velocity_y = plane_flap_velocity
                    plane_flapped = True
    
        game_over = isGameOver(horizontal, vertical,
                               up_obstacles, down_obstacles)
        if game_over:
            print("Game Over!")
            window.blit(game_images['gameover'], (0,0))
            pygame.display.update()
            time.sleep(1.5)
            return
  
        playerMidPos = horizontal + game_images['plane'].get_width()/2
        for obstacle in up_obstacles:
            obstacleMidPos = obstacle['x'] + game_images['obstacleimage'][0].get_width()/2
            if obstacleMidPos <= playerMidPos < obstacleMidPos + 4:
                your_score += 1
                print(f"Your your_score is {your_score}")
  
        if plane_velocity_y < plane_Max_Vel_Y and not plane_flapped:
            plane_velocity_y += planeAccY
  
        if plane_flapped:
            plane_flapped = False
        playerHeight = game_images['plane'].get_height()
        vertical = vertical + \
            min(plane_velocity_y, elevation - vertical - playerHeight)
  
        for upperobstacle, lowerobstacle in zip(up_obstacles, down_obstacles):
            upperobstacle['x'] += obstacleVelX
            lowerobstacle['x'] += obstacleVelX
  
        if 0 < up_obstacles[0]['x'] < 5:
            newobstacle = createobstacle()
            up_obstacles.append(newobstacle[0])
            down_obstacles.append(newobstacle[1])

        if up_obstacles[0]['x'] < -game_images['obstacleimage'][0].get_width():
            up_obstacles.pop(0)
            down_obstacles.pop(0)
  
        window.blit(game_images['background'], (0, 0))
        for upperobstacle, lowerobstacle in zip(up_obstacles, down_obstacles):
            window.blit(game_images['obstacleimage'][0],
                        (upperobstacle['x'], upperobstacle['y']))
            window.blit(game_images['obstacleimage'][1],
                        (lowerobstacle['x'], lowerobstacle['y']))
  
        window.blit(game_images['land_level'], (ground, elevation))
        window.blit(game_images['plane'], (horizontal, vertical))
  
        numbers = [int(x) for x in list(str(your_score))]
        width = 0
  
        for num in numbers:
            width += game_images['scoreimages'][num].get_width()
        Xoffset = (window_width - width)/1.1
  
        for num in numbers:
            window.blit(game_images['scoreimages'][num],
                        (Xoffset, window_width*0.02))
            Xoffset += game_images['scoreimages'][num].get_width()
  
        pygame.display.update()
        framepersecond_clock.tick(framepersecond)
  
  
def isGameOver(horizontal, vertical, up_obstacles, down_obstacles):
    if vertical > elevation - 25 or vertical < 0:
        return True
  
    for obstacle in up_obstacles:
        obstacleHeight = game_images['obstacleimage'][0].get_height()
        if(vertical < obstacleHeight + obstacle['y'] and\
           abs(horizontal - obstacle['x']) < game_images['obstacleimage'][0].get_width()):
            return True
  
    for obstacle in down_obstacles:
        if (vertical + game_images['plane'].get_height() > obstacle['y']) and\
        abs(horizontal - obstacle['x']) < game_images['obstacleimage'][0].get_width():
            return True
    return False
  
  
def createobstacle():
    offset = window_height/3
    obstacleHeight = game_images['obstacleimage'][0].get_height()
    y2 = offset + random.randrange(
            0, int(window_height - game_images['land_level'].get_height() - 1.2 * offset))  
    obstacleX = window_width + 10
    y1 = obstacleHeight - y2 + offset
    obstacle = [
        # upper obstacle
        {'x': obstacleX, 'y': -y1},
        # lower obstacle
        {'x': obstacleX, 'y': y2}
    ]
    return obstacle
  
if __name__ == "__main__":
  
    pygame.init()
    framepersecond_clock = pygame.time.Clock()
  
    pygame.display.set_caption('PyPlane Game')
  
    game_images['scoreimages'] = (
        pygame.image.load('images/0.png').convert_alpha(),
        pygame.image.load('images/1.png').convert_alpha(),
        pygame.image.load('images/2.png').convert_alpha(),
        pygame.image.load('images/3.png').convert_alpha(),
        pygame.image.load('images/4.png').convert_alpha(),
        pygame.image.load('images/5.png').convert_alpha(),
        pygame.image.load('images/6.png').convert_alpha(),
        pygame.image.load('images/7.png').convert_alpha(),
        pygame.image.load('images/8.png').convert_alpha(),
        pygame.image.load('images/9.png').convert_alpha()
    )
    game_images['plane'] = pygame.image.load(planeplayer_image).convert_alpha()
    
    game_images['land_level'] = pygame.image.load(land_image).convert_alpha()
    
    game_images['background'] = pygame.image.load(background_image).convert_alpha()
    
    #game_images['start'] = pygame.image.load(start_image).convert_alpha()

    game_images['obstacleimage'] = (pygame.transform.rotate(pygame.image.load(
        obstacle_image).convert_alpha(), 180), pygame.image.load(
      obstacle_image).convert_alpha())
    
    game_images['gameover'] = pygame.image.load(game_over).convert_alpha()
  
    print("WELCOME TO PYPLANE GAME")
    print("Press space or enter to start the game")
  
    while True:
  
        horizontal = int(window_width/5)
        vertical = int(
            (window_height - game_images['plane'].get_height())/2)
        ground = 0
        while True:
            for event in pygame.event.get():
                #window.blit(game_images['start'], (0,0))

                if event.type == QUIT or (event.type == KEYDOWN and \
                                          event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
  
                elif event.type == KEYDOWN and (event.key == K_SPACE or\
                                                event.key == K_UP):
                    flappygame()
  
                else:
                    window.blit(game_images['background'], (0, 0))
                    window.blit(game_images['plane'],
                                (horizontal, vertical))
                    window.blit(game_images['land_level'], (ground, elevation))
                    pygame.display.update()
                    framepersecond_clock.tick(framepersecond)