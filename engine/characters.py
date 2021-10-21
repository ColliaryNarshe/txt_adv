import random

class ValueRange:
    # This isn't used yet.
    group_a_slimes = [1, 5]
    group_b_slimes = [1, 6]
    group_c_slimes = [1, 5]
    group_c_goblins = [0, 4]
    group_d_goblins = [0, 4]
    group_d_goblin_mage = [1, 2]
    group_e_ork = [1, 3]
    group_f_ork = [1, 3]
    group_f_goblin_mage = [0, 3]
    group_goblin_king = [2,2]
    group_goblin_king_goblin = [0, 2]
    group_boss_slim = [1,2]


class Character:
    def __init__(self, name, health, mp, attack, defense, speed, target):
        self.name = name
        self.health = health
        self.health_max = self.health
        self.mp = mp
        self.mp_max = mp
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.target = target # chance to get targeted (or could do based on opponent type instead)
        self.dead = False
        self.damage_lost = 0


def init_characters():
                               #HP  MP Att Def Sp target
    a = Character('Knight',     250, 0, 20, .5, 10, 10)
    b = Character('Archer',     200, 0, 14, .3, 15, 4)
    c = Character('Thief',      160, 0,  10, .2, 20, 3)
    d = Character('White Mage', 110, 100, 3, .1, 5, 2)
    e = Character('Black Mage', 120, 140, 30, .1, 5, 3)

    character_list = [a,b,c,d,e]
    # Return ValueRange without parenthesis so it can be edited in engine and
    # affect here (with parenthesis will make a separate instance)
    return character_list

# Ordered by speed of chars

class Enemies:
    def __init__(self, type):
        if type == 'Goblin':
            self.name = 'Goblin'
            self.health = 30
            self.defense = .2
            self.attack = 7
            self.speed = 8
            self.target = 10

        if type == 'Goblin Mage':
            self.name = 'Goblin Mage'
            self.health = 50
            self.defense = .3
            self.attack = 12
            self.speed = 10
            self.target = 12

        if type == 'Ork':
            self.name = 'Ork'
            self.health = 50
            self.defense = .4
            self.attack = 15
            self.speed = 10
            self.target = 8

        if type == 'Slime':
            self.name = 'Slime'
            self.health = 17
            self.defense = .75
            self.attack = 6
            self.speed = 1
            self.target = 10

        if type == 'Goblin King':
            self.name = 'Goblin King'
            self.health = 100
            self.defense = .7
            self.attack = 30
            self.speed = 15
            self.target = 5

        if type == 'Slime King':
            self.name = 'Slime King'
            self.health = 350
            self.defense = .8
            self.attack = 35
            self.speed = 5
            self.target = 5


def enemy_group(group):
    # Added to list in order of speed
    if group == 'Group A':
        num = random.randint(2,5) # Slimes
        group_list = []
        for _ in range(num):
            group_list.append(Enemies('Slime'))
        return group_list

    if group == 'Group B':
        num = random.randint(2,4) # Goblins
        group_list = []
        for _ in range(num):
            group_list.append(Enemies('Goblin'))
        return group_list

    if group == 'Group C':
        num = random.randint(2,4) # Slimes
        num2 = random.randint(1,3) # Goblins
        group_list = []
        for _ in range(num2):
            group_list.append(Enemies('Goblin'))
        for _ in range(num):
            group_list.append(Enemies('Slime'))
        return group_list

    if group == 'Group D':
        num = random.randint(1,4) # Goblins
        num2 = random.randint(2,2) # Goblin Mage
        group_list = []
        for _ in range(num):
            group_list.append(Enemies('Goblin'))
        for _ in range(num2):
            group_list.append(Enemies('Goblin Mage'))
        return group_list

    if group == 'Group E':
        num = random.randint(2,4) # Ork
        group_list = []
        for _ in range(num):
            group_list.append(Enemies('Ork'))
        return group_list

    if group == 'Group F':
        num = random.randint(1,3) # Ork
        num2 = random.randint(0,2) # Goblin Mage
        group_list = []
        for _ in range(num):
            group_list.append(Enemies('Ork'))
        for _ in range(num2):
            group_list.append(Enemies('Goblin Mage'))
        return group_list

    if group == 'Group Goblin King':
        num = random.randint(2,2) # Goblin King
        num2 = random.randint(0,1) # Goblin
        group_list = []
        for _ in range(num):
            group_list.append(Enemies('Goblin King'))
        for _ in range(num2):
            group_list.append(Enemies('Goblin'))
        return group_list

    if group == 'Group Boss': # Slime King Boss + Slime
        num = random.randint(0,0)
        group_list = []
        group_list.append(Enemies('Slime King'))
        for _ in range(num):
            group_list.append(Enemies('Slime'))
        return group_list
