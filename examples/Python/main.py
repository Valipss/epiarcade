import pygame
import json, os

# Load basic window
pygame.init()
DISPLAY_W, DISPLAY_H = 960, 570
canvas = pygame.Surface((DISPLAY_W,DISPLAY_H))
window = pygame.display.set_mode(((DISPLAY_W,DISPLAY_H)))
running = True
player = pygame.Rect(DISPLAY_W/2, DISPLAY_H/2, 60,60)
LEFT, RIGHT, UP, DOWN = False, False, False, False
clock = pygame.time.Clock()
color = 0

# Initialize controller
joysticks = []
for i in range(pygame.joystick.get_count()):
    joysticks.append(pygame.joystick.Joystick(i))
for joystick in joysticks:
    joystick.init()

analog_keys = {0:0, 1:0, 2:0, 3:0, 4:-1, 5: -1 }

# Start game loop
while running:
    # Check player input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            pass

        # Handles button presses
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 0:
                print('ok')
                LEFT = True
            if event.button == 1:
                print('ok')
                RIGHT = True
            if event.button == 2:
                print('ok')
                DOWN = True
            if event.button == 3:
                print('ok')
                UP = True
        # Handles button releases
        if event.type == pygame.JOYBUTTONUP:
            if event.button == 0:
                LEFT = False
            if event.button == 1:
                RIGHT = False
            if event.button == 2:
                DOWN = False
            if event.button == 3:
                UP = False

        # Handled analg inputs
        if event.type == pygame.JOYAXISMOTION:
            analog_keys[event.axis] = event.value
            # Horizontal Analog
            if abs(analog_keys[0]) > .4:
                if analog_keys[0] < -.7:
                    LEFT = True
                else:
                    LEFT = False
                if analog_keys[0] > .7:
                    RIGHT = True
                else:
                    RIGHT = False
            # Vertical Analog
            if abs(analog_keys[1]) > .4:
                if analog_keys[1] < -.7:
                    UP = True
                else:
                    UP = False
                if analog_keys[1] > .7:
                    DOWN = True
                else:
                    DOWN = False

    # Handle Player movement
    if LEFT:
        player.x -=5
    if RIGHT:
        player.x += 5
    if UP:
        player.y -= 5
    if DOWN:
        player.y += 5

    if color < 0:
        color = 0
    elif color > 255:
        color = 255

    # Update window and display
    canvas.fill((255,255,255))
    pygame.draw.rect(canvas, (0,0 + color,255), player)
    window.blit(canvas, (0,0))
    clock.tick(60)
    pygame.display.update()