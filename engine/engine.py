import textwrap
import random
from engine.characters import init_characters, enemy_group
from engine.battle import battle
import pygame

WRAP_NUM = 59
console_lines = 13

class Engine:
    def __init__(self, room_list):
        self.character_list = init_characters()  # Returns character instances
        self.current_room = room_list[1]
        self.previous_room = None
        self.room_list = room_list
        self.complete_text = []  # Console txt
        self.game_over = False
        self.restart = False
        self.menu_state = 'main'
        self.character_selection = ''  # This and current_item used together to give a  selected character an item # Also with inventory menu, heal magic
        self.current_item = ''
        self.option = 'undecided'  # 'yes', 'no', or 'undecided'
        self.chosen_char = False  # For choosing characters on selection screen
        self.nothing_of_interest = True # when inspecting
        self.just_left = False  # Used for inspect to not show the "nothing of interest" after getting item with menu
        self.door_locked = True
        self.left_choice = True
        self.zoom = True
        self.enemy_left_or_right = random.choice(['left', 'right'])  # Wanted it sent at start of game to make the choice more real.

        # Sound effects: (Using channels in case menu sound effect is playing while moving sound effect)
        pygame.mixer.set_num_channels(2)
        self.channel = pygame.mixer.Channel(1) # For walking
        self.menu_sound = pygame.mixer.Sound("sounds/menu.wav")
        self.battle_sound = pygame.mixer.Sound("sounds/defeatedenemy.mp3")
        self.running_sound = pygame.mixer.Sound("sounds/running.mp3")
        self.healing_sound = pygame.mixer.Sound("sounds/save.mp3")
        self.walking_sound = pygame.mixer.Sound("sounds/walking.mp3")
        self.chest_sound = pygame.mixer.Sound("sounds/chest.mp3")
        self.found_treasure_sound = pygame.mixer.Sound("sounds/KHitem.mp3")
        self.error_sound = pygame.mixer.Sound("sounds/error.mp3")

        # pygame.event.wait()

        self.room_enter_states = {'enter': True,
                                  'battle': False,
                                  'text': False,
                                  'inspect_enter': True,
                                  'special_choice': False,
                                  'inspect_treasure': False,
                                 }

        self.item_inventory = [['Potion', 3],
                               ['Ether', 0],
                               ['Elixir', 0],
                               ['Knife', 0],
                               ['Sword', 0],
                               ['Light Armor', 0],
                               ['Defense Ring', 0],
                               ['Strength Ring', 0],
                               ['Map', 0],
                               ['Key', 0],
                               ['Black Staff', 0],
                               ['Oak Staff', 0],
                               ['Silver Bow', 0]
                              ]
        self.trap_types = ['an arrow trap', 'a fire trap', 'a hidden pit trap', 'a falling rock trap', 'a swinging axe trap']
        self.specials_text = {
            'Fountain':
                    [
                     [' ', "RED:You have found a mysterious fountain.", "Drink the water?"],
                     ["Cautious, perhaps wise.", ' ']
                    ],
            'Shrine':
                    [
                     [' ', "RED:You have found a mysterious shrine.", "Will you pray to it?"],
                     ["Who knows who will hear these prayers, better to leave it be.", ' ']
                    ],
            'Unidentified Potion':
                    [
                     [' ', "RED:You have found an Unidentified Potion.", "Will you drink it?"],
                     ["You leave the potion behind.", ' ']
                    ]
        }

        self.diff_level = {
            'traps': [10, 16],  # Max 16 (based on chosen rooms)
            'special': [2, 6],  # Max 7
            'potions': [5, 8],  # Max 13
            'treasures': [4, 7],  # Max 10
            'enemiesA': [7, 13],  # Max 21 (both enemies combined)
            'enemiesB': [4, 7]  # Harder than A
        }


        # self.seed_number = 0
        self.item_placement_calc()

        # Print the location of things to console, just for testing:
        for room in self.room_list[1:]:
            txt = f"Room {room.location}: \n"
            if room.special:
                txt += '    Special:  ' + room.special + '\n'
            if room.treasure:
                txt += '    Treasure: ' + ', '.join(room.treasure) + '\n'
            if room.trap: txt += f"    Trap:     {room.trap}\n"
            if room.enemies:
                txt += "    Enemies:  ("
                for enemy in room.enemies:
                    txt += enemy.name + ', '
                txt = txt.strip()
                txt += ")"
            if len(txt) <= 10:
                txt += "    EMPTY"
            txt = txt.strip()
            print(txt)


    def heal_magic(self):
        # Check if enough MP, not dead, and target's health is not full or dead:
        if self.character_list[3].mp >= 20 and not self.character_list[3].dead and self.character_selection.health != self.character_selection.health_max and not self.character_selection.dead:
            # Check if Oak staff equiped:
            to_add = 50
            for item in self.item_inventory:
                if item[0] == 'Oak Staff' and item[1]:
                    to_add = 100
            # Add health and remove MP
            self.character_selection.health += to_add
            self.character_list[3].mp -= 20
            # If health goes over max, set it to max
            if self.character_selection.health > self.character_selection.health_max:
                self.character_selection.health = self.character_selection.health_max

            self.update_console([f"{self.character_selection.name} has gained 50HP. White Mage has lost 20MP"])
            self.healing_sound.play()
            self.healing_sound.set_volume(.3)
        else:
            self.error_sound.play()
            self.error_sound.set_volume(.3)
            self.update_console([f"You can't do that."])


    def item_placement_calc(self):
        tier_one_enemy_groups = ['Group A', 'Group B', 'Group C']
        tier_two_enemy_groups = ['Group D', 'Group E', 'Group F']

        def place_items(all_items, poss_locations, low, high, trap=False, special=False):
            number = random.randint(low, high)
            random.shuffle(all_items)
            treasures_chosen = all_items[:number]
            # if special, can take items more than once
            if special:
                treasures_chosen = []
                for _ in range(number):
                    treasures_chosen.append(random.choice(all_items))
            for treasure in treasures_chosen:
                room = random.choice(poss_locations)
                poss_locations.remove(room)
                # Traps or treasure
                if trap:
                    self.room_list[room].trap = True
                elif special:
                    self.room_list[room].special = treasure
                else:
                    self.room_list[room].treasure.append(treasure)

        # Items hard coded: Key 14, Shrine 15, Nothing 20 (locked door), Enemies 14,20,26

        # Special items: -----------------------
        special_items_choices = ['Fountain', 'Fountain', 'Shrine', 'Unidentified Potion']
        special_rooms_poss = [6, 7, 12, 13, 19, 21, 24]
        place_items(special_items_choices, special_rooms_poss, self.diff_level['special'][0], self.diff_level['special'][1], special=True)

        # Traps rooms: --------------------------
        traps_possible = [3, 4, 5, 7, 8, 9, 11, 12, 13, 14, 16, 18, 19, 21, 23, 24]
        place_items([True for x in range(11)], traps_possible, self.diff_level['traps'][0], self.diff_level['traps'][1], True)

        # Treasures & Potions ------------------------- # Map is set at room 24
        all_potion_items = ['Potion' for x in range(12)]
        all_treasure_items = ['Knife', 'Sword', 'Silver Bow', 'Black Staff', 'Oak Staff', 'Light Armor', 'Defense Ring', 'Strength Ring', 'Ether', 'Ether', 'Elixir']

        # Possible rooms to use:
        all_potion_locations =   [3, 5, 6, 7, 9, 11, 13, 16, 18, 19, 21, 23, 24]
        all_treasure_locations = [3, 5, 7, 9, 11, 16, 18, 19, 21, 23]

        place_items(all_potion_items, all_potion_locations, self.diff_level['potions'][0], self.diff_level['potions'][1])
        place_items(all_treasure_items, all_treasure_locations, self.diff_level['treasures'][0], self.diff_level['treasures'][1])
        # Enemies--------------------------
        # Number of enemy groups to spread around map
        enemy_encounters_A_num = random.randint(self.diff_level['enemiesA'][0], self.diff_level['enemiesA'][1])
        enemy_encounters_B_num = random.randint(self.diff_level['enemiesB'][0], self.diff_level['enemiesB'][1])

        # Get a list of random rooms matching number of enemy groups:
        # Rooms 14 and 20 removed for mini bosses
        poss_rooms = [2,3,4,5,6,7,8,9,10,11,12,13,15,16,17,18,19,21,22,23,24]
        random.shuffle(poss_rooms)

        enemy_rooms_A = poss_rooms[:enemy_encounters_A_num]
        temp_rooms = poss_rooms[enemy_encounters_A_num:]
        enemy_rooms_B = temp_rooms[:enemy_encounters_B_num]

        for enemy_idx in enemy_rooms_A:
            group = random.choice(tier_one_enemy_groups)
            self.room_list[enemy_idx].enemies = enemy_group(group)
        for enemy_idx in enemy_rooms_B:
            group = random.choice(tier_two_enemy_groups)
            self.room_list[enemy_idx].enemies = enemy_group(group)

        # 2 Goblin Kings in room 14 (with key), and two in 20 (locked door)
        self.room_list[14].enemies = enemy_group('Group Goblin King')
        self.room_list[20].enemies = enemy_group('Group Goblin King')

        # Boss (Slime King + 2-4 Slimes)
        self.room_list[26].enemies = enemy_group('Group Boss')


    def enter_room(self):
        '''
        Prints the game text to the console:
        '''

        if self.current_room.trap:
            self.trap_run()


        if self.current_room.enemies:
            if self.room_enter_states['enter']: # First
                self.fight_or_run()
                self.room_enter_states['enter'] = False
                self.room_enter_states['battle'] = True
            elif self.room_enter_states['battle']: # Second
                self.check_enemy_encounter()
                self.room_enter_states['battle'] = False
                self.room_enter_states['text'] = True
        elif not self.game_over:
            # When no enemies, displays text
            self.display_room_txt()
            if self.current_room.location == 25:
                self.menu_state = 'left_right'


        # Displays text after enemies defeated:
        if self.room_enter_states['text'] and not self.game_over and self.current_room != 26: # Third
            self.display_room_txt()
            self.room_enter_states['enter'] = True
            self.room_enter_states['text'] = False


    def specials_handle(self):
        """Changes menu and states for special item choices: """
        type = self.current_room.special
        if self.room_enter_states['inspect_enter']:
            self.nothing_of_interest = False
            self.update_console(self.specials_text[type][0])  # Got an key error HERE from accessing dict
            self.menu_state = 'choice'
            self.room_enter_states['inspect_enter'] = False
            self.room_enter_states['special_choice'] = True

        if self.room_enter_states['special_choice']:
            if self.option == 'yes':
                self.nothing_of_interest = False
                # Change menu back:
                self.menu_state = 'main'
                # Reset option variable for future choices:
                self.option = 'undecided'
                # Change inspection state:
                self.room_enter_states['special_choice'] = False
                self.room_enter_states['inspect_enter'] = True
                self.room_enter_states['inspect_treasure'] = True
                # Remove special from room list:
                self.current_room.special = []
                # Writes the text based on fountain type:
                self.special_calc(type)

            if self.option == 'no':
                self.update_console(self.specials_text[type][1])
                self.nothing_of_interest = False
                self.menu_state = 'main'
                self.option = 'undecided'
                self.room_enter_states['inspect_enter'] = True
                self.room_enter_states['special_choice'] = False
                self.room_enter_states['inspect_treasure'] = True
                if not self.current_room.treasure:
                    self.room_enter_states['inspect_treasure'] = False


    def add_current_item(self):
        for item in self.item_inventory:
            if item[0] == self.current_item:
                item[1] += 1
        self.item_character_choice()
        self.just_left = True


    def item_character_choice(self):
        """Handles equipping items to characters."""

        if self.current_item == 'Defense Ring':
            if self.chosen_char:
                if not self.character_selection.dead:
                    self.update_console([self.character_selection.name + "'s defense has gone up!", ' '])
                    self.character_selection.defense += .2
                    self.chosen_char = False
                    self.menu_state = 'main'
                else:
                    self.error_sound.play()
                    self.error_sound.set_volume(.3)
            else:
                self.update_console([f"RED:You received a Defense Ring!", "Who will equip it?"])
                self.menu_state = 'characters'

        elif self.current_item == 'Strength Ring':
            if self.chosen_char:
                if not self.character_selection.dead:
                    self.update_console([self.character_selection.name + "'s strength has gone up!", ' '])
                    self.character_selection.attack += 10
                    self.chosen_char = False
                    self.menu_state = 'main'
                else:
                    self.error_sound.play()
                    self.error_sound.set_volume(.3)
            else:
                self.update_console([f"RED:You received a Strength Ring!", "Who will equip it?"])
                self.menu_state = 'characters'

        elif self.current_item == 'Knife':
            self.update_console(["RED:You found a Knife!"])
            self.character_list[2].attack += 10  # Given bonus even if dead, in case revived
            if not self.character_list[2].dead:
                self.update_console([f"{self.character_list[2].name}'s damage and his chance to disarm traps has increased!"])
            else:
                self.update_console([f"You can't use it because {self.character_list[2].name} is dead."])


        elif self.current_item == 'Sword':
            self.update_console(["RED:You found a Sword!"])
            self.character_list[0].attack += 15
            if not self.character_list[0].dead:
                self.update_console([f"{self.character_list[0].name}'s damage has greatly increased!"])
            else:
                self.update_console([f"You can't use it because {self.character_list[0].name} is dead."])


        elif self.current_item == 'Black Staff':
            self.update_console(["RED:You found a Black Staff!"])
            self.character_list[4].attack += 15
            if not self.character_list[4].dead:
                self.update_console([f"{self.character_list[4].name}'s damage has greatly increased!"])
            else:
                self.update_console([f"You can't use it because {self.character_list[4].name} is dead."])


        elif self.current_item == 'Oak Staff':
            self.update_console(["RED:You found an Oak Staff!"])
            self.character_list[3].attack += 3
            if not self.character_list[3].dead:
                self.update_console([f"{self.character_list[3].name}'s healing power has doubled!"])
            else:
                self.update_console([f"You can't use it because {self.character_list[3].name} is dead."])


        elif self.current_item == 'Silver Bow':
            self.update_console(["RED:You found a Silver Bow!"])
            self.character_list[1].attack += 10
            self.character_list[1].defense += .5
            if not self.character_list[1].dead:
                self.update_console([f"{self.character_list[1].name}'s attack and defense have increased!"])
            else:
                self.update_console([f"You can't use it because {self.character_list[1].name} is dead."])


        elif self.current_item == 'Light Armor':
            if self.chosen_char:
                if not self.character_selection.dead:
                    self.update_console([self.character_selection.name + "'s strength has gone up!", ' '])
                    self.character_selection.defense += .3
                    self.chosen_char = False
                    self.menu_state = 'main'
                else:
                    self.error_sound.play()
                    self.error_sound.set_volume(.3)
            else:
                self.update_console(["RED:You received Light Armor!", "Who will equip it?"])
                self.menu_state = 'characters'

        # Any other treasure:
        else:
            self.update_console([f"RED:Recieved a {self.current_item}!", ' '])

        self.just_left = True


    def special_calc(self, type):

        def mp_recovery():
            # Used for Magic Fountain or Magic Shrine
            alive = False
            txt_names = ''

            if not self.character_list[3].dead:
                alive = True
                self.character_list[3].mp += 50
                if self.character_list[3].mp >= self.character_list[3].mp_max:
                    self.character_list[3].mp = self.character_list[3].mp_max
                txt_names = f"{self.character_list[4].name} has gained 50HP"

            if not self.character_list[4].dead:
                alive = True
                self.character_list[4].mp += 50
                if self.character_list[4].mp >= self.character_list[4].mp_max:
                    self.character_list[4].mp = self.character_list[4].mp_max
                if txt_names:
                    txt_names = "Both wizards have gained 50MP"
                else:
                    txt_names = f"{self.character_list[4].name} has gained 50HP"

            if txt_names:
                self.update_console([txt_names])
            # If no mages alive, add health instead
            if not alive:
                chosen_fount = 'Health'

        live_characters = [x for x in self.character_list if not x.dead]
        char_hit = random.choice(live_characters)
        damage = random.randint(5, 60)
        health = random.randint(10, 150)

        # If Special is FOUNTAIN =======================
        if type == 'Fountain':
            fount_types = ['Black', 'Health', 'Magic', 'Black', 'Health', 'Magic', 'Ring']
            chosen_fount = random.choice(fount_types)

            # Ring Fountain ------------------------
            if chosen_fount == 'Ring':
                ring_choice = random.choice(['Defense Ring', 'Strength Ring'])
                self.current_item = ring_choice
                self.update_console(["As you reach down to drink, you see something golden glittering under the water."])
                self.add_current_item()

            # Black fountain ----------------------
            if chosen_fount == 'Black':
                self.update_console(["You approach the fountain, but quickly realize the water is black and putrid. You jump back just as a tentacle shoots out to attack your party", f"{char_hit.name} loses {damage}HP.", ' '])
                char_hit.health -= damage
                if char_hit.health < 1:
                    char_hit.health = 0
                    char_hit.dead = True
                    self.update_console([f"RED:{char_hit.name} has died!", ' '])

            # Magic Fountain -----------------------
            if chosen_fount == 'Magic':
                mp_recovery()

            # Health Fountain ---------------
            if chosen_fount == 'Health':
                for char in live_characters:
                    if not char.dead:
                        char.health += health
                    if char.health > char.health_max:
                        char.health = char.health_max
                self.update_console([f"Your entire party feels refreshed after drinking the clear water. Gained {health}HP each.", ' '])

        # If Special is SHRINE ==============================
        if type == 'Shrine':
            shrine_types = ['Health', 'Magic', 'Weakness', 'Death']
            chosen_shrine = random.choice(shrine_types)

            # Health Shrine ----------------
            if chosen_shrine == 'Health':
                for char in live_characters:
                    if not char.dead:
                        char.health += health
                    if char.health > char.health_max:
                        char.health = char.health_max
                self.update_console([f"A light envolopes your party, and they feel energized. Gained {health}HP each.", ' '])

            if chosen_shrine == 'Magic':
                mp_recovery()

            if chosen_shrine == 'Weakness':
                char_hit.defense -= .2
                self.update_console([f"An eerie darkness rises from the shrine. {char_hit.name} has become weak.", ' '])

            if chosen_shrine == 'Death':
                life_left = random.randint(0,1)
                char_hit.health = life_left
                if life_left == 1:
                    self.update_console([f"A black beam hits {char_hit.name}, knocking him to the floor. He is barely holding on to life.", ' '])
                else:
                    self.update_console([f"A black beam hits {char_hit.name}, knocking him to the floor. You quickly check on him and find him dead.", ' '])
                    char_hit.dead = True

        # If Special is UNIDENTIFIED POTION ==================================
        if type == 'Unidentified Potion':
            potion = random.randint(0,1)

            if potion == 1:
                char_hit.health += 100
                if char_hit.health > char_hit.health_max:
                    char_hit.health = char_hit.health_max
                self.update_console([f"{char_hit.name} has regained 100HP.", ' '])

            if potion == 0:
                char_hit.health -= 50
                self.update_console([f"{char_hit.name} has lost 50HP.", ' '])
                if char_hit.health < 0:
                    char_hit.health = 0
                    char_hit.dead = True
                    self.update_console([f"RED:{char_hit.name} has died!", ' '])


    def get_treasure(self):
        # When treasure chest found, changes menu to 'choice' to open chest
        if self.room_enter_states['inspect_treasure'] and not self.room_enter_states['special_choice'] and not self.menu_state =='characters':
            if self.option == 'undecided':
                self.found_treasure_sound.play()
                self.found_treasure_sound.set_volume(.5)
                self.nothing_of_interest = False
                self.menu_state = 'choice'
                self.update_console([f"You found a treasure chest. Would you like to open it?", ' '])

            if self.option == 'yes':
                self.chest_sound.play()
                self.chest_sound.set_volume(.5)
                self.nothing_of_interest = False
                self.menu_state = 'main'
                for treasure in self.current_room.treasure:
                    self.current_item = treasure
                    self.add_current_item()
                self.current_room.treasure = []
                self.option = 'undecided'
                self.room_enter_states['inspect_treasure'] = False

            if self.option == 'no':
                self.nothing_of_interest = False
                self.menu_state = 'main'
                self.update_console([f"You leave the chest unopened.", ' '])
                self.option = 'undecided'
                self.room_enter_states['inspect_treasure'] = False


    def inspect_room(self):

        self.nothing_of_interest = True

        # Specials: ----------------------------------------
        if self.current_room.special and self.room_enter_states['inspect_treasure'] == False:
            self.specials_handle()

        if not self.current_room.special:
            self.room_enter_states['inspect_treasure'] = True

        # Treasure Chests: ----------------------------------
        if self.current_room.treasure:
            self.get_treasure()

        # Unlock the door:
        if self.current_room.location == 20:  # Correct room
            if self.current_room.lock:  # Door not already unlocked
                for item in self.item_inventory:
                    if item[0] == 'Key' and item[1]:  # If there's a map.
                        self.current_room.lock = False
                        self.update_console(["-==-You've unlocked the door with the key!-==-", ' '])
                        self.door_locked = False

        # Message to get a key:
        if self.current_room.location == 20 and self.current_room.lock:
            # Note: This will run twice if there is an item in room with options, so I just disable treasures/specials here...
            self.update_console(["--You need to find a key!--", ' '])
        else:
            # Found nothing: (Any room) ------------------------------
            if self.nothing_of_interest and not self.just_left:

                self.update_console([self.current_room.inspect_txt, ' '])
            else:
                self.just_left = False


    def update_console(self, new: list):
        # Shorten length if too long:
        for line in new:
            if line.startswith('RED:'):
                colored = textwrap.fill(line[4:], WRAP_NUM, drop_whitespace=False).splitlines()
                for line in colored:
                    self.complete_text.append('RED:' + line.strip())
            else:
                self.complete_text += textwrap.fill(line, WRAP_NUM, drop_whitespace=False).splitlines()

        self.complete_text = self.complete_text[-console_lines:]

        # Get rid of whitespace (created with textwrap or splitlines?)
        stripped_list = []
        for line in self.complete_text:  # =Indent= to put spaces with character damage txt
            line = line.strip()
            stripped_list.append(line)
        self.complete_text = stripped_list


    def check_enemy_encounter(self):
        new = []

        # Battle: ------------------
        died, self.game_over = battle(self.character_list, self.current_room.enemies)

        # Display damage on two lines:
        temp_string = 'Damage: '
        temp_string2 = ''
        if not self.character_list[0].dead: temp_string += f"Knight:  {int(self.character_list[0].damage_lost)}  "
        if not self.character_list[1].dead: temp_string += f"     Archer:  {int(self.character_list[1].damage_lost)} "
        if not self.character_list[2].dead: temp_string += f"    Thief: {int(self.character_list[2].damage_lost)}"
        if not self.character_list[3].dead: temp_string2 = f"=Indent=White Mage:  {int(self.character_list[3].damage_lost)}  "
        if not self.character_list[4].dead: temp_string2 += f"  Black Mage: {int(self.character_list[4].damage_lost)}"
        new += [temp_string] + [temp_string2] + [' ']
        for char in self.character_list:
            char.damage_lost = 0

        # Display which characters died:
        died_chars = 'RED:'
        for d in died:
            died_chars += f"{d} has died!  "

        new += [died_chars]
        # Display result of battle:
        if self.game_over:
            new += ["YOU LOST THE GAME!", ' ']
        else:
            new += ["You defeated the enemies!", ' ']
        self.current_room.enemies = []
        # Add new text to console
        self.update_console(new)
        self.room_enter_states['battle'] = False
        self.room_enter_states['text'] = True
        self.battle_sound.play()
        self.battle_sound.set_volume(.3)


    def display_room_txt(self):
        # Get default text from room (first or second time in room)
        # new = ["----------"]
        if self.current_room.first_time:
            new = [self.current_room.first_enter_txt, ' ']
            self.current_room.first_time = False
        else:
            new = [self.current_room.return_txt, ' ']

        self.update_console(new)


    def trap_run(self):
        # If Thief is alive, 50% chance of disable, 75% with Knife equiped:
        num_chance = 2
        # Check for knife:
        for item in self.item_inventory:
            if item[0] == 'Knife' and item[1]:
                num_chance = 3

        if not self.character_list[2].dead and random.randint(0,3) < num_chance:
                self.update_console(['RED:Your thief disabled a trap.', ' '])
        else:
            # Choose character from live characters:
            live_characters = [x for x in self.character_list if not x.dead]
            char_hit = random.choice(live_characters)
            # Damage:
            damage = random.randint(5, 15)
            char_hit.health -= damage
            # Trap name:
            trap_type = random.choice(self.trap_types)
            # Message to console:
            txt = f'RED:{char_hit.name} got hit by {trap_type} and lost {damage}HP!'
            self.update_console([txt, ' '])
            # If character dies from trap:
            if char_hit.health < 1:
                char_hit.health = 0
                char_hit.dead = True
                self.update_console([f'RED:{char_hit.name} has died!', ' '])

        self.current_room.trap = []


    def fight_or_run(self):
        enemy_names = [x.name for x in self.current_room.enemies]
        new = [f"You have enountered: {', '.join(enemy_names)}", 'Do you want to fight?', ' ']
        self.update_console(new)
        self.menu_state = 'choice'


    def last_room(self):
        self.display_room_txt()
        self.game_over = True


    def split_room(self):
        self.menu_state = 'main'
        if self.enemy_left_or_right == 'left':  # Enemy on the left
            if self.left_choice:  # Chose to go left
                char = random.choice([x for x in self.character_list if not x.dead])
                char.health = 1
                self.update_console(['There is a cave-in!', f"{char.name} is seriously injured!"])
            else:  # Chose to go right
                self.update_console(['You pass through the room uneventfully.'])

        elif self.enemy_left_or_right == 'right':  # Enemy on right
            if not self.left_choice:  # Chose to go right
                char = random.choice([x for x in self.character_list if not x.dead])
                char.health = 1
                self.update_console(['There is a cave-in!', f"{char.name} is seriously injured!"])
            else:  # Chose to go left
                self.update_console(['You pass through the room uneventfully.'])
