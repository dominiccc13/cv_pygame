"""
Socket Server
"""
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setblocking(False)
sock.bind(("0.0.0.0", 3000))

def get_command():
    try:
        data, _ = sock.recvfrom(1024)
        return data.decode().split(",")
    except:
        return None

"""
# Game #
"""
import pygame as pg

pg.init()

width, height = 800, 600
screen = pg.display.set_mode((width, height))
pg.display.set_caption("Obstacle Game")

bg = pg.image.load("bg.jpg").convert()
bg_width, bg_height = bg.get_width(), bg.get_height()
bg_x, bg_y = 0, 0
scroll_speed = .2

player = pg.Rect(width//2, height//2, 30, 30)
speed = 3

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

fps = 120
clock = pg.time.Clock()

running = True
while running:
    # Event handling
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            pass

    # Game state
    cmd = get_command()
    if cmd:
        print(cmd)
        if cmd[0] == "w":
            multiplier = 2.5 if cmd[1] == "True" else 1
            bg_y += speed*multiplier
        if cmd[0] == "wa":
            multiplier = 2.5 if cmd[1] == "True" else 1
            bg_y += 2.5*multiplier
            player.x -= 1.67*multiplier
        if cmd[0] == "wd":
            multiplier = 2.5 if cmd[1] == "True" else 1
            bg_y += 2.5*multiplier
            player.x += 1.67*multiplier
        if cmd[0] == "a":
            multiplier = 2 if cmd[1] == "True" else 1
            player.x -= speed*multiplier
        if cmd[0] == "d":
            multiplier = 2 if cmd[1] == "True" else 1
            player.x += speed*multiplier
        if cmd[0] == "s":
            multiplier = 2.5 if cmd[1] == "True" else 1
            bg_y -= speed*multiplier
        if cmd[0] == "sa":
            multiplier = 2.5 if cmd[1] == "True" else 1
            bg_y -= 2.5*multiplier
            player.x -= 1.67*multiplier
        if cmd[0] == "sd":
            multiplier = 2.5 if cmd[1] == "True" else 1
            bg_y -= 2.5*multiplier
            player.x += 1.67*multiplier

    bg_x %= bg_width
    bg_y %= bg_height

    for i in range(-1, 2):
        for j in range(-1, 2):
            screen.blit(bg, (i*bg_width + bg_x - bg_width, j*bg_height + bg_y - bg_height))

    # Sending to server

    # Drawing
    # screen.fill(BLACK)
    player.y = height//2 - player.height//2
    pg.draw.rect(screen, (255,0,0), player)

    # Update the display
    pg.display.flip()

    # Cap the frame rate
    clock.tick(fps)

# Quit Pygame
pg.quit()