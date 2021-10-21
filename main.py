import pygame
pygame.init()

from engine.panes import Panes
from engine.keyboard_input import keyboard_input
from engine.engine_rooms import init_rooms


# If you change FPS it will alter speed of scrolling when holding down arrows
FPS = 10
BACKGROUND_COLOR = 'grey30'

# Window:
WIN = pygame.display.set_mode((1400,1000))
pygame.display.set_caption("RPG")
time = pygame.time.Clock()

# Add start text (also initializes room data):
engine = init_rooms()
engine.enter_room()
panes = Panes(WIN, engine)
panes.action_menu.disable_menus()

while True:
    time.tick(FPS)
    fullscreen = keyboard_input(panes, engine)
    if engine.restart:
        # Restart game
        engine = init_rooms()
        engine.enter_room()
        panes = Panes(WIN, engine)
        panes.action_menu.disable_menus()

    # if fullscreen:  # For fullscreen will need to make fog of war rects adjustable sizes rather than set.
    #     panes = Panes(WIN, engine)
    #     panes.action_menu.disable_menus()
    #     fullscreen = False

    panes.display_screen()

    pygame.display.update()
