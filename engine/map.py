import pygame

class Map:
    def __init__(self, map_width, map_height, zoom=False):
        self.MAP_WIDTH = map_width
        self.MAP_HEIGHT = map_height
        self.current_room = 1
        if zoom: x = 2
        else: x = 1

        self.fog_dict = {
            2: [int(map_width * .12), int(map_height * .59), 87*x, 127*x],
            3: [int(map_width * .08), int(map_height * .69), 40*x, 50*x],
            4: [int(map_width * .19), int(map_height * .65), 150*x, 50*x],
            5: [int(map_width * .34), int(map_height * .66), 70*x, 50*x],
            6: [int(map_width * .255), int(map_height * .45), 140*x, 100*x],
            7: [int(map_width * .19), int(map_height * .47), 55*x, 50*x],
            8: [int(map_width * .10), int(map_height * .40), 80*x, 95*x],
            9: [int(map_width * .09), int(map_height * .425), 52*x, 55*x],
            9.12: [int(map_width * .06), int(map_height * .4), 77*x, 55*x],
            10: [int(map_width * .152), int(map_height * .26), 70*x, 90*x],
            11: [int(map_width * .16), int(map_height * .15), 80*x, 80*x],
            12: [int(map_width * .05), int(map_height * .25), 92*x, 84*x],
            13: [int(map_width * .06), int(map_height * .13), 85*x, 76*x],
            14: [int(map_width * .01), int(map_height * .09), 47*x, 60*x],
            15: [int(map_width * .38), int(map_height * .46), 190*x, 90*x],
            16: [int(map_width * .56), int(map_height * .43), 40*x, 50*x],
            17: [int(map_width * .40), int(map_height * .33), 140*x, 70*x],
            18: [int(map_width * .26), int(map_height * .33), 165*x, 70*x],
            19: [int(map_width * .40), int(map_height * .16), 110*x, 87*x],
            20: [int(map_width * .55), int(map_height * .25), 130*x, 100*x],
            21: [int(map_width * .675), int(map_height * .32), 60*x, 60*x],
            22: [int(map_width * .58), int(map_height * .19), 100*x, 30*x],
            23: [int(map_width * .54), int(map_height * .17), 45*x, 45*x],
            24: [int(map_width * .65), int(map_height * .02), 110*x, 110*x],
            25: [int(map_width * .775), int(map_height * 0), 140*x, 120*x],
            26: [int(map_width * .90), int(map_height * .07), 100*x, 110*x],
            27: [int(map_width * .89), int(map_height * .02), 67*x, 45*x],

        }
        self.rooms_dict = {1: [int(map_width * .2), int(map_height * .92)],
                           2: [int(map_width * .16), int(map_height * .72)],
                           3: [int(map_width * .10), int(map_height * .73)],
                           4: [int(map_width * .31), int(map_height * .70)],
                           5: [int(map_width * .40), int(map_height * .70)],
                           6: [int(map_width * .31), int(map_height * .55)],
                           7: [int(map_width * .23), int(map_height * .53)],
                           8: [int(map_width * .17), int(map_height * .49)],
                           9: [int(map_width * .13), int(map_height * .46)],
                           10: [int(map_width * .19), int(map_height * .37)],
                           11: [int(map_width * .21), int(map_height * .21)],
                           12: [int(map_width * .12), int(map_height * .36)],
                           13: [int(map_width * .12), int(map_height * .20)],
                           14: [int(map_width * .04), int(map_height * .14)],
                           15: [int(map_width * .50), int(map_height * .56)],
                           16: [int(map_width * .58), int(map_height * .49)],
                           17: [int(map_width * .51), int(map_height * .40)],
                           18: [int(map_width * .29), int(map_height * .41)],
                           19: [int(map_width * .46), int(map_height * .25)],
                           20: [int(map_width * .61), int(map_height * .37)],
                           21: [int(map_width * .70), int(map_height * .39)],
                           22: [int(map_width * .62), int(map_height * .23)],
                           23: [int(map_width * .57), int(map_height * .22)],
                           24: [int(map_width * .74), int(map_height * .13)],
                           25: [int(map_width * .83), int(map_height * .12)],
                           26: [int(map_width * .94), int(map_height * .17)],
                           27: [int(map_width * .92), int(map_height * .07)]
        }
        # Load map:
        self.map_original = pygame.image.load('maps/DunGen1.jpg').convert_alpha()
        self.map = pygame.transform.scale(self.map_original, (self.MAP_WIDTH, self.MAP_HEIGHT))
        # Icons + locations
        self.lock_x = int(map_width * .61)
        self.lock_y = int(map_height * .28)
        self.lock = pygame.image.load('icons/lock0.png').convert_alpha()
        self.lock = pygame.transform.scale(self.lock, (30,30))
        self.lock.set_colorkey((255,255,255))

        self.unlocked_x = int(map_width * .597)
        self.unlocked_y = int(map_height * .28)
        self.unlocked = pygame.image.load('icons/unlocked0.png').convert_alpha()
        self.unlocked = pygame.transform.scale(self.unlocked, (35,35))
        # self.image.set_colorkey((255,255,255))

        self.key_x = int(map_width * .015)
        self.key_y = int(map_height * .105)
        self.key = pygame.image.load('icons/key.png').convert_alpha()
        self.key = pygame.transform.scale(self.key, (35,35))
