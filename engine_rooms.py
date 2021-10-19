from engine import Engine


class Room1:
    def __init__(self):
        self.location = 1
        self.first_enter_txt = "You and your party of adventurers enter the dark dungeon, weapons in hand. You look around cautiously, careful to see if you spot any enemies or traps. You take a deep breath, and decide to explore for treasure."
        self.first_time = True
        self.return_txt = "You have returned to the entrance. Has fear gripped your sense of adventure?"
        self.inspect_txt = "The dim light from the entrance lights up the stone walls of a barren room. A darker path leads into a hallway. It's not too late to leave this dungeon unharmed, but the promise of fortune urges you on."

        self.trap = False
        self.enemies = []
        self.treasure = []
        self.special = ''
        self.fog_on = True

                      #      N S W E
        self.room_choices = [2,0,0,0]



class Room2:
    def __init__(self):
        self.first_enter_txt = "You find yourself in a split path. Which dark corridor will you choose?"
        self.first_time = True
        self.return_txt = "You have returned to the four-way pass."
        self.location = 2
        self.inspect_txt = "These halls are confusing, you had better be careful."

        self.trap = False
        self.enemies = []
        self.treasure = []
        self.special = ''
        self.fog_on = True

        self.room_choices = [8,1,3,4]


class Room3:
    def __init__(self):
        self.first_enter_txt = "Even dead ends should be search thoroughly."
        self.first_time = True
        self.return_txt = "You have returned to this dead end, but it looks much the same."
        self.location = 3
        self.inspect_txt = "There is nothing else of interest."

        self.trap = False
        self.enemies = []
        self.treasure = []
        self.special = ''
        self.fog_on = True

        self.room_choices = [0,0,0,2]


class Room4:
    def __init__(self):
        self.first_enter_txt = "Two choices seem to lay before you."
        self.first_time = True
        self.return_txt = "Two choices seem to lay before you."
        self.location = 4
        self.inspect_txt = "There is nothing else of interest."

        self.trap = False
        self.enemies = []
        self.treasure = []
        self.special = ''
        self.fog_on = True

        self.room_choices = [6,0,2,5]



class Room5:
    def __init__(self):
        self.first_enter_txt = "This hall leads nowhere, but is there treasure?"
        self.first_time = True
        self.return_txt = "This is the wrong way."
        self.location = 5
        self.inspect_txt = "There is nothing else of interest."

        self.trap = False
        self.enemies = []
        self.treasure = []
        self.special = ''
        self.fog_on = True

        self.room_choices = [0,0,4,0]



class Room6:
    def __init__(self):
        self.first_enter_txt = "The narrow stone walls open up to a room so large and dark you cannot see the end of it. The walls are made of mud here and there is a bottomless pit you dare not go near. You start to regret entering this dungeon."
        self.first_time = True
        self.return_txt = "You have returned to the mud pit room."
        self.location = 6
        self.inspect_txt = "There is nothing else here, except a feeling of dread."

        self.trap = False
        self.enemies = []
        self.treasure = []
        self.special = ''
        self.fog_on = True

        self.room_choices = [0,4,7,15]


class Room7:
    def __init__(self):
        self.first_enter_txt = "You find a small chamber with racks of old weapons and armor, but they are too rusted to be of any value."
        self.first_time = True
        self.return_txt = "You've returned to old weapon's room."
        self.location = 7
        self.inspect_txt = "Was this chamber some sort of storage room?"

        self.trap = False
        self.enemies = []
        self.treasure = []
        self.special = ''
        self.fog_on = True

        self.room_choices = [0,0,8,6]


class Room8:
    def __init__(self):
        self.first_enter_txt = "Another four-way split. Be careful not to lose your bearings."
        self.first_time = True
        self.return_txt = "Choose correctly."
        self.location = 8
        self.inspect_txt = "There is nothing else of interest."

        self.trap = False
        self.enemies = []
        self.treasure = []
        self.special = ''
        self.fog_on = True

        self.room_choices = [10,2,9,7]


class Room9:
    def __init__(self):
        self.first_enter_txt = "You enter an oddly shaped room filled with columns. There are too many dark spaces for comfort."
        self.first_time = True
        self.return_txt = "You're back in the column room"
        self.location = 9
        self.inspect_txt = "You search every corner and column, but there is nothing left of interest."

        self.trap = False
        self.enemies = []
        self.treasure = []
        self.special = ''
        self.fog_on = True

        self.room_choices = [0,0,0,8]


class Room10:
    def __init__(self):
        self.first_enter_txt = "The narrow hallway opens up to a wider chamber with a high ceiling. You watch your footing as you walk across the uneven footing of broken stone slabs."
        self.first_time = True
        self.return_txt = "You've returned to the open hallway."
        self.location = 10
        self.inspect_txt = "There is nothing else of interest."

        self.trap = False
        self.enemies = []
        self.treasure = []
        self.special = ''
        self.fog_on = True

        self.room_choices = [11,8,12,0]


class Room11:
    def __init__(self):
        self.first_enter_txt = "Down a long hallway you find a promising room. Surely there is treasure here."
        self.first_time = True
        self.return_txt = "This is a dead end."
        self.location = 11
        self.inspect_txt = "There is nothing else of interest."

        self.trap = False
        self.enemies = []
        self.treasure = []
        self.special = ''
        self.fog_on = True

        self.room_choices = [0,10,0,0]


class Room12:
    def __init__(self):
        self.first_enter_txt = "This large room has a smaller chamber in the middle with a blocked entrance by stone rubble. Inside you can see countless stone statues, most of which are broken. Perhaps you can come back here to escavate them someday."
        self.first_time = True
        self.return_txt = "Stone statue room."
        self.location = 12
        self.inspect_txt = "There is nothing else of interest here except the stone statues, but they are too hard to get to and too heavy to carry."

        self.trap = False
        self.enemies = []
        self.treasure = []
        self.special = ''
        self.fog_on = True

        self.room_choices = [13,0,0,10]


class Room13:
    def __init__(self):
        self.first_enter_txt = "You enter a part of the dungeon that is in the worst shape so far. There is nothing but dirt, broken pillars, and caveins. It will be difficult to make a path and avoid the pits, but you think you see a path through."
        self.first_time = True
        self.return_txt = "You return to this broken room with a sigh of regret."
        self.location = 13
        self.inspect_txt = "There is nothing else of interest among the rubble."

        self.trap = False
        self.enemies = []
        self.treasure = []
        self.special = ''
        self.fog_on = True

        self.room_choices = [0,12,14,0]


class Room14:
    def __init__(self):
        self.first_enter_txt = "You find a simple room that looks to have been used as a sleeping quarter. In the back you see a wooden chest, and you wet your lip expectantly."
        self.first_time = True
        self.return_txt = "The simple room."
        self.location = 14
        self.inspect_txt = "There is nothing else besides that key. It is made of gold, so it has some value at least."

        self.trap = False
        self.enemies = []
        self.treasure = ['Key']
        self.special = ''
        self.fog_on = True

        self.room_choices = [0,0,0,13]


class Room15:
    def __init__(self):
        self.first_enter_txt = "You approach the center of the room, where you see a ten foot statue on a stone dais. You don't recognize the old god this belongs to, and wonder whether to approach further and pay your respects."
        self.first_time = True
        self.return_txt = "You have returned to the shrine room."
        self.location = 15
        self.inspect_txt = "There is nothing else besides the altar, which captures all the attention from the room.."

        self.trap = False
        self.enemies = []
        self.treasure = []
        self.special = 'Shrine'
        self.fog_on = True

        self.room_choices = [17,0,6,16]


class Room16:
    def __init__(self):
        self.first_enter_txt = "Another dead end, but worth investigating."
        self.first_time = True
        self.return_txt = "You can't go this way."
        self.location = 16
        self.inspect_txt = "There is nothing else of interest."

        self.trap = False
        self.enemies = []
        self.treasure = []
        self.special = ''
        self.fog_on = True

        self.room_choices = [0,15,0,0]


class Room17:
    def __init__(self):
        self.first_enter_txt = "The path opens up to a four-way split. Which way will you choose first?"
        self.first_time = True
        self.return_txt = "You've returned to the four-way split."
        self.location = 17
        self.inspect_txt = "There is nothing else of interest."

        self.trap = False
        self.enemies = []
        self.treasure = []
        self.special = ''
        self.fog_on = True

        self.room_choices = [19,15,18,20]


class Room18:
    def __init__(self):
        self.first_enter_txt = "You walk down what feels like a neverending tunnel. The darkness of the hall and heat from your torch begin to grate on your nerves, but you remain optimistic. Finally you reach the end, where you see a small chamber."
        self.first_time = True
        self.return_txt = "You've returned down the dark hallway again, hopefully for good reason."
        self.location = 18
        self.inspect_txt = "There is nothing else of interest."

        self.trap = False
        self.enemies = []
        self.treasure = []
        self.special = ''
        self.fog_on = True

        self.room_choices = [0,0,0,17]


class Room19:
    def __init__(self):
        self.first_enter_txt = "This stone chamber is largely empty, but there are dark corners worth exploring."
        self.first_time = True
        self.return_txt = "You have returned to the large chamber room."
        self.location = 19
        self.inspect_txt = "You shine your torch over every nook and cranny, but find nothing else."

        self.trap = False
        self.enemies = []
        self.treasure = []
        self.special = ''
        self.fog_on = True

        self.room_choices = [0,17,0,0]


class Room20:
    def __init__(self):
        self.first_enter_txt = "Directly in front of you is a small wooden doorway, but you barely notice it with the imposing iron gate atop stone steps to the north. There will be no brute-forcing your way through it, but you notice a keyhole..."
        self.first_time = True
        self.return_txt = "You've returned to the iron gate room."
        self.location = 20
        self.inspect_txt = "There is nothing else of interest."
        self.lock = True

        self.trap = False
        self.enemies = []
        self.treasure = []
        self.special = ''
        self.fog_on = True

        self.room_choices = [22,0,17,21]


class Room21:
    def __init__(self):
        self.first_enter_txt = "You enter a chamber divided by a small creek running out of the southern wall. The other side of the creek has some places to inspect, and you decide it is worth getting your feet wet."
        self.first_time = True
        self.return_txt = "You've returned to the creek room."
        self.location = 21
        self.inspect_txt = "There is nothing else of interest, and now your boots are sloshing."

        self.trap = False
        self.enemies = []
        self.treasure = []
        self.special = ''
        self.fog_on = True

        self.room_choices = [0,0,20,0]


class Room22:
    def __init__(self):
        self.first_enter_txt = "The hallway splits between the left and right"
        self.first_time = True
        self.return_txt = "You've returned to the three-way split."
        self.location = 22
        self.inspect_txt = "Nothing to do here except choose a path."

        self.trap = False
        self.enemies = []
        self.treasure = []
        self.special = ''
        self.fog_on = True

        self.room_choices = [0,20,23,24]


class Room23:
    def __init__(self):
        self.first_enter_txt = "You've reached a dead end, and hope it wasn't in vain."
        self.first_time = True
        self.return_txt = "You cannot go farther."
        self.location = 23
        self.inspect_txt = "There is nothing else of interest."

        self.trap = False
        self.enemies = []
        self.treasure = []
        self.special = ''
        self.fog_on = True

        self.room_choices = [0,0,0,22]


class Room24:
    def __init__(self):
        self.first_enter_txt = "You are reminded of the part of the dungeon where you found the key, dilapidated and falling apart. You wonder if this is even still the same dungeon, or if you've wandered into a cave system."
        self.first_time = True
        self.return_txt = "You've returned to the dilapidated chamber"
        self.location = 24
        self.inspect_txt = "There is nothing else of interest."

        self.trap = False
        self.enemies = []
        self.treasure = ['Map']
        self.special = ''
        self.fog_on = True

        self.room_choices = [0,0,22,25]


class Room25:
    def __init__(self):
        self.first_enter_txt = "You enter the room, finding two winding paths stretching in opposite directions. Will you go left or right?"
        self.first_time = True
        self.return_txt = "You take the same path as before, afraid of what fate the other might hold."
        self.location = 25
        self.inspect_txt = "There is nothing else of interest."

        self.trap = False
        self.enemies = []
        self.treasure = []
        self.special = ''
        self.fog_on = True

        self.room_choices = [0,0,24,26]


class Room26:
    def __init__(self):
        self.first_enter_txt = "You walk down a hall that reminds you of an ancient king's throne room, lined with columns. As you walk past the columns, a dark shape becomes clearer in the distance. At least twenty feet tall, you can't tell what this blob shaped object is. Until it moves, jiggles. You ready your weapon, as you've never encountered such a large slime monster before."
        self.first_time = True
        self.return_txt = ""
        self.location = 26
        self.inspect_txt = "The Slime King's corpse is now only a puddle of goo."

        self.trap = False
        self.enemies = []
        self.treasure = []
        self.special = ''
        self.fog_on = True

        self.room_choices = [27,0,25,0]


class Room27:
    def __init__(self):
        self.first_enter_txt = "Inside a small room that was likely once hidden, you find stairs leading into a treasury. Inside you find gold, gems, diamonds, and all manner of piceless weapons and armor. Despite the hardship, you have found more reward than you hoped for. Now, how to make it back?"
        self.first_time = True
        self.return_txt = ""
        self.location = 27
        self.inspect_txt = ""

        self.trap = False
        self.enemies = []
        self.treasure = []
        self.special = ''
        self.fog_on = True

        self.room_choices = [0,26,0,0]



def init_rooms():
    room1 = Room1()
    room2 = Room2()
    room3 = Room3()
    room4 = Room4()
    room5 = Room5()
    room6 = Room6()
    room7 = Room7()
    room8 = Room8()
    room9 = Room9()
    room10 = Room10()
    room11 = Room11()
    room12 = Room12()
    room13 = Room13()
    room14 = Room14()
    room15 = Room15()
    room16 = Room16()
    room17 = Room17()
    room18 = Room18()
    room19 = Room19()
    room20 = Room20()
    room21 = Room21()
    room22 = Room22()
    room23 = Room23()
    room24 = Room24()
    room25 = Room25()
    room26 = Room26()
    room27 = Room27()

    room_list = [None, room1, room2, room3, room4, room5, room6, room7, room8, room9, room10, room11, room12, room13, room14, room15, room16, room17, room18, room19, room20, room21, room22, room23, room24, room25, room26, room27]
    engine = Engine(room_list)
    return engine
